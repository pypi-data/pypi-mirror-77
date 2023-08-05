import * as p from "@bokehjs/core/properties";
import { div, canvas } from "@bokehjs/core/dom";
import { HTMLBox } from "@bokehjs/models/layouts/html_box";
import { clone } from "@bokehjs/core/util/object";
import { PanelHTMLBoxView, set_size } from "../layout";
import { vtkns, majorAxis, applyStyle } from "./util";
import { VTKColorBar } from "./vtkcolorbar";
const INFO_DIV_STYLE = {
    padding: "0px 2px 0px 2px",
    maxHeight: "150px",
    height: "auto",
    backgroundColor: "rgba(255, 255, 255, 0.4)",
    borderRadius: "10px",
    margin: "2px",
    boxSizing: "border-box",
    overflow: "hidden",
    overflowY: "auto",
    transition: "width 0.1s linear",
    bottom: "0px",
    position: "absolute",
};
export class AbstractVTKView extends PanelHTMLBoxView {
    initialize() {
        super.initialize();
        this._camera_callbacks = [];
        this._renderable = true;
        this._setting_camera = false;
    }
    _add_colorbars() {
        //construct colorbars
        const old_info_div = this.el.querySelector(".vtk_info");
        if (old_info_div)
            this.el.removeChild(old_info_div);
        if (this.model.color_mappers.length < 1)
            return;
        const info_div = document.createElement("div");
        const expand_width = "350px";
        const collapsed_width = "30px";
        info_div.classList.add('vtk_info');
        applyStyle(info_div, INFO_DIV_STYLE);
        applyStyle(info_div, { width: expand_width });
        this.el.appendChild(info_div);
        //construct colorbars
        const colorbars = [];
        this.model.color_mappers.forEach((mapper) => {
            const cb = new VTKColorBar(info_div, mapper);
            colorbars.push(cb);
        });
        //content when collapsed
        const dots = document.createElement('div');
        applyStyle(dots, { textAlign: "center", fontSize: "20px" });
        dots.innerText = "...";
        info_div.addEventListener('click', () => {
            if (info_div.style.width === collapsed_width) {
                info_div.removeChild(dots);
                applyStyle(info_div, { height: "auto", width: expand_width });
                colorbars.forEach((cb) => info_div.appendChild(cb.canvas));
            }
            else {
                colorbars.forEach((cb) => info_div.removeChild(cb.canvas));
                applyStyle(info_div, { height: collapsed_width, width: collapsed_width });
                info_div.appendChild(dots);
            }
        });
        info_div.click();
    }
    connect_signals() {
        super.connect_signals();
        this.on_change(this.model.properties.orientation_widget, () => {
            this._orientation_widget_visibility(this.model.orientation_widget);
        });
        this.on_change(this.model.properties.camera, () => this._set_camera_state());
        this.on_change(this.model.properties.axes, () => {
            this._delete_axes();
            if (this.model.axes)
                this._set_axes();
            this._vtk_render();
        });
        this.on_change(this.model.properties.color_mappers, () => this._add_colorbars());
    }
    render() {
        super.render();
        if (!this._vtk_renwin || !this._vtk_container) {
            this._orientationWidget = null;
            this._axes = null;
            this._vtk_container = div();
            this.init_vtk_renwin();
            set_size(this._vtk_container, this.model);
            this.el.appendChild(this._vtk_container);
            this._connect_interactions_to_model();
            this._remove_default_key_binding();
            this._bind_key_events();
            this.plot();
            this._add_colorbars();
            this.model.renderer_el = this._vtk_renwin;
        }
        else {
            set_size(this._vtk_container, this.model);
            // warning if _vtk_renwin contain controllers or other elements 
            // we must attach them to the new el
            this.el.appendChild(this._vtk_container);
        }
    }
    after_layout() {
        super.after_layout();
        if (this._renderable)
            this._vtk_renwin.resize(); // resize call render method
        this._vtk_render();
    }
    invalidate_render() {
        this._unsubscribe_camera_cb();
        super.invalidate_render();
    }
    remove() {
        this._unsubscribe_camera_cb();
        window.removeEventListener("resize", this._vtk_renwin.resize);
        this._vtk_renwin.delete();
        super.remove();
    }
    get _vtk_camera_state() {
        const vtk_camera = this._vtk_renwin.getRenderer().getActiveCamera();
        let state;
        if (vtk_camera) {
            state = clone(vtk_camera.get());
            delete state.classHierarchy;
            delete state.vtkObject;
            delete state.vtkCamera;
            delete state.viewPlaneNormal;
            delete state.flattenedDepIds;
            delete state.managedInstanceId;
            delete state.directionOfProjection;
            delete state.projectionMatrix;
            delete state.viewMatrix;
            delete state.physicalTranslation;
            delete state.physicalScale;
            delete state.physicalViewUp;
            delete state.physicalViewNorth;
            delete state.mtime;
        }
        return state;
    }
    get _axes_canvas() {
        let axes_canvas = this._vtk_container.querySelector(".axes-canvas");
        if (!axes_canvas) {
            axes_canvas = canvas({
                style: {
                    position: "absolute",
                    top: "0",
                    left: "0",
                    width: "100%",
                    height: "100%",
                },
            });
            axes_canvas.classList.add("axes-canvas");
            this._vtk_container.appendChild(axes_canvas);
            this._vtk_renwin.setResizeCallback(() => {
                if (this._axes_canvas) {
                    const dims = this._vtk_container.getBoundingClientRect();
                    const width = Math.floor(dims.width * window.devicePixelRatio);
                    const height = Math.floor(dims.height * window.devicePixelRatio);
                    this._axes_canvas.setAttribute("width", width.toFixed());
                    this._axes_canvas.setAttribute("height", height.toFixed());
                }
            });
        }
        return axes_canvas;
    }
    _bind_key_events() {
        this.el.addEventListener("mouseenter", () => {
            const interactor = this._vtk_renwin.getInteractor();
            if (this.model.enable_keybindings) {
                document
                    .querySelector("body")
                    .addEventListener("keypress", interactor.handleKeyPress);
                document
                    .querySelector("body")
                    .addEventListener("keydown", interactor.handleKeyDown);
                document
                    .querySelector("body")
                    .addEventListener("keyup", interactor.handleKeyUp);
            }
        });
        this.el.addEventListener("mouseleave", () => {
            const interactor = this._vtk_renwin.getInteractor();
            document
                .querySelector("body")
                .removeEventListener("keypress", interactor.handleKeyPress);
            document
                .querySelector("body")
                .removeEventListener("keydown", interactor.handleKeyDown);
            document
                .querySelector("body")
                .removeEventListener("keyup", interactor.handleKeyUp);
        });
    }
    _connect_interactions_to_model() {
        // update camera model state only at the end of the interaction
        // with the scene (avoid bouncing events and large amount of events)
        const update_model_camera = () => {
            this._get_camera_state();
            this.model.properties.camera.change.emit();
        };
        const interactor = this._vtk_renwin.getInteractor();
        const event_list = ["LeftButtonRelease", "RightButtonRelease", "EndAnimation"];
        event_list.forEach((event) => interactor['on' + event](update_model_camera));
    }
    _create_orientation_widget() {
        const axes = vtkns.AxesActor.newInstance();
        // add orientation widget
        this._orientationWidget = vtkns.OrientationMarkerWidget.newInstance({
            actor: axes,
            interactor: this._vtk_renwin.getInteractor(),
        });
        this._orientationWidget.setEnabled(true);
        this._orientationWidget.setViewportCorner(vtkns.OrientationMarkerWidget.Corners.BOTTOM_RIGHT);
        this._orientationWidget.setViewportSize(0.15);
        this._orientationWidget.setMinPixelSize(75);
        this._orientationWidget.setMaxPixelSize(300);
        this._widgetManager = vtkns.WidgetManager.newInstance();
        this._widgetManager.setRenderer(this._orientationWidget.getRenderer());
        const widget = vtkns.InteractiveOrientationWidget.newInstance();
        widget.placeWidget(axes.getBounds());
        widget.setBounds(axes.getBounds());
        widget.setPlaceFactor(1);
        const vw = this._widgetManager.addWidget(widget);
        // Manage user interaction
        vw.onOrientationChange(({ direction }) => {
            const camera = this._vtk_renwin.getRenderer().getActiveCamera();
            const focalPoint = camera.getFocalPoint();
            const position = camera.getPosition();
            const viewUp = camera.getViewUp();
            const distance = Math.sqrt(Math.pow(position[0] - focalPoint[0], 2) +
                Math.pow(position[1] - focalPoint[1], 2) +
                Math.pow(position[2] - focalPoint[2], 2));
            camera.setPosition(focalPoint[0] + direction[0] * distance, focalPoint[1] + direction[1] * distance, focalPoint[2] + direction[2] * distance);
            if (direction[0])
                camera.setViewUp(majorAxis(viewUp, 1, 2));
            if (direction[1])
                camera.setViewUp(majorAxis(viewUp, 0, 2));
            if (direction[2])
                camera.setViewUp(majorAxis(viewUp, 0, 1));
            this._vtk_renwin.getRenderer().resetCameraClippingRange();
            this._vtk_render();
        });
        this._orientation_widget_visibility(this.model.orientation_widget);
    }
    _delete_axes() {
        if (this._axes) {
            Object.keys(this._axes).forEach((key) => this._vtk_renwin.getRenderer().removeActor(this._axes[key]));
            this._axes = null;
            const textCtx = this._axes_canvas.getContext("2d");
            if (textCtx)
                textCtx.clearRect(0, 0, this._axes_canvas.clientWidth * window.devicePixelRatio, this._axes_canvas.clientHeight * window.devicePixelRatio);
        }
    }
    _get_camera_state() {
        if (!this._setting_camera) {
            this._setting_camera = true;
            this.model.camera = this._vtk_camera_state;
            this._setting_camera = false;
        }
    }
    _orientation_widget_visibility(visibility) {
        this._orientationWidget.setEnabled(visibility);
        if (visibility)
            this._widgetManager.enablePicking();
        else
            this._widgetManager.disablePicking();
        this._vtk_render();
    }
    _remove_default_key_binding() {
        const interactor = this._vtk_renwin.getInteractor();
        document
            .querySelector("body")
            .removeEventListener("keypress", interactor.handleKeyPress);
        document
            .querySelector("body")
            .removeEventListener("keydown", interactor.handleKeyDown);
        document
            .querySelector("body")
            .removeEventListener("keyup", interactor.handleKeyUp);
    }
    _set_axes() {
        if (this.model.axes && this._vtk_renwin.getRenderer()) {
            const { psActor, axesActor, gridActor } = this.model.axes.create_axes(this._axes_canvas);
            this._axes = { psActor, axesActor, gridActor };
            this._vtk_renwin.getRenderer().addActor(psActor);
            this._vtk_renwin.getRenderer().addActor(axesActor);
            this._vtk_renwin.getRenderer().addActor(gridActor);
        }
    }
    _set_camera_state() {
        if (!this._setting_camera) {
            this._setting_camera = true;
            if (this.model.camera &&
                JSON.stringify(this.model.camera) != JSON.stringify(this._vtk_camera_state))
                this._vtk_renwin
                    .getRenderer()
                    .getActiveCamera()
                    .set(this.model.camera);
            this._vtk_renwin.getRenderer().resetCameraClippingRange();
            this._vtk_render();
            this._setting_camera = false;
        }
    }
    _unsubscribe_camera_cb() {
        this._camera_callbacks
            .splice(0, this._camera_callbacks.length)
            .map((cb) => cb.unsubscribe());
    }
    _vtk_render() {
        if (this._renderable) {
            if (this._orientationWidget)
                this._orientationWidget.updateMarkerOrientation();
            this._vtk_renwin.getRenderWindow().render();
        }
    }
}
AbstractVTKView.__name__ = "AbstractVTKView";
export class AbstractVTKPlot extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    getActors() {
        return this.renderer_el.getRenderer().getActors();
    }
    static init_AbstractVTKPlot() {
        this.define({
            axes: [p.Instance],
            camera: [p.Instance],
            color_mappers: [p.Array, []],
            orientation_widget: [p.Boolean, false],
        });
        this.override({
            height: 300,
            width: 300,
        });
    }
}
AbstractVTKPlot.__name__ = "AbstractVTKPlot";
AbstractVTKPlot.__module__ = "panel.models.vtk";
AbstractVTKPlot.init_AbstractVTKPlot();
//# sourceMappingURL=vtklayout.js.map