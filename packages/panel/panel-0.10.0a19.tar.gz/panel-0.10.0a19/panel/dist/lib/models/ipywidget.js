import * as p from "@bokehjs/core/properties";
import { HTMLBox } from "@bokehjs/models/layouts/html_box";
import { PanelHTMLBoxView } from "./layout";
const Jupyter = window.Jupyter;
export class IPyWidgetView extends PanelHTMLBoxView {
    constructor() {
        super(...arguments);
        this.rendered = false;
    }
    render() {
        super.render();
        if (!this.rendered) {
            this._render().then(() => {
                this.rendered = true;
                this.invalidate_layout();
                this.notify_finished();
            });
        }
    }
    has_finished() {
        return this.rendered && super.has_finished();
    }
    async _render() {
        const { spec, state } = this.model.bundle;
        let manager;
        if ((Jupyter != null) && (Jupyter.notebook != null))
            manager = Jupyter.notebook.kernel.widget_manager;
        else if (window.PyViz.widget_manager != null)
            manager = window.PyViz.widget_manager;
        if (!manager) {
            console.log("Panel IPyWidget model could not find a WidgetManager");
            return;
        }
        const models = await manager.set_state(state);
        const model = models.find((item) => item.model_id == spec.model_id);
        if (model != null) {
            const view = await manager.create_view(model, { el: this.el });
            if (view.children_views) {
                for (const child of view.children_views.views)
                    await child;
            }
            this.el.appendChild(view.el);
            view.trigger('displayed', view);
        }
    }
}
IPyWidgetView.__name__ = "IPyWidgetView";
export class IPyWidget extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_IPyWidget() {
        this.prototype.default_view = IPyWidgetView;
        this.define({
            bundle: [p.Any, {}],
        });
    }
}
IPyWidget.__name__ = "IPyWidget";
IPyWidget.__module__ = "panel.models.ipywidget";
IPyWidget.init_IPyWidget();
//# sourceMappingURL=ipywidget.js.map