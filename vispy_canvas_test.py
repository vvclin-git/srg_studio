import numpy as np
from vispy import app, scene
from vispy.color import Color


class CircleVisual(scene.visuals.Ellipse):
    def __init__(self, center, radius, **kwargs):
        super().__init__(center=center, radius=(radius, radius),
                         color=Color('#e88834'), border_color='white', **kwargs)
        self.interactive = True


class PolygonVisual(scene.visuals.Polygon):
    def __init__(self, vertices, **kwargs):
        super().__init__(pos=vertices, color=Color('#34a8e8'), border_color='white', **kwargs)
        self.interactive = True


class Canvas(scene.SceneCanvas):
    def __init__(self):
        super().__init__(keys='interactive', size=(800, 900))
        self.unfreeze()

        self.grid = self.central_widget.add_grid()
        self.view = self.grid.add_view(row=0, col=0, row_span=8)
        self.view.camera = scene.PanZoomCamera(rect=(-100, -100, 200, 200), aspect=1.0)

        # Output text field below canvas
        self.console = scene.visuals.Text("Mouse actions will appear here.", color='white', anchor_x='left', parent=self.view.scene, pos=(10, -90))

        # List of visual objects
        self.shapes = []
        self.selected = None
        self.drag_start = None

        self.timer = app.Timer('auto', connect=self.update_scene, start=True)

        scene.visuals.GridLines(parent=self.view.scene)

        # Connect events explicitly
        self.events.mouse_press.connect(self.on_mouse_press)
        self.events.mouse_release.connect(self.on_mouse_release)
        self.events.mouse_move.connect(self.on_mouse_move)

        self.freeze()
        self.show()

    def update_scene(self, event=None):
        # Real-time check of all shapes, can log or analyze here
        shape_info = f"Tracking {len(self.shapes)} shapes..."
        # You can extend this to send updates to a logger or UI

    def log(self, text):
        self.console.text = text

    def on_mouse_press(self, event):
        pos = self.scene.node_transform(self.view.scene).map(event.pos)
        self.view.interactive = False
        hit = self.visual_at(event.pos)
        self.view.interactive = True

        if event.button == 1:
            if hit is not None and any(hit is s or hit in s.children for s in self.shapes):
                # Match visual or its children
                self.selected = next(s for s in self.shapes if hit is s or hit in s.children)
                self.drag_start = pos
                self.log(f"Left click on shape at {pos.round(2)} - start drag")
            else:
                self.selected = None
                self.view.camera.interactive = True
                self.log(f"Left click on empty at {pos.round(2)} - pan mode")

        elif event.button == 2:
            self.log(f"Right click at {pos.round(2)} - no action")

    def on_mouse_release(self, event):
        self.selected = None
        self.view.camera.interactive = False
        self.drag_start = None

    def on_mouse_move(self, event):
        if event.is_dragging and self.selected is not None and self.drag_start is not None:
            current_pos = self.scene.node_transform(self.view.scene).map(event.pos)
            delta = current_pos - self.drag_start

            if isinstance(self.selected, CircleVisual):
                self.selected.center = self.selected.center + delta
            elif isinstance(self.selected, PolygonVisual):
                self.selected.pos += delta

            self.drag_start = current_pos
            self.log(f"Dragging shape to {current_pos.round(2)}")

    def add_circle(self, center, radius):
        circle = CircleVisual(center=center, radius=radius, parent=self.view.scene)
        self.shapes.append(circle)

    def add_polygon(self, vertices):
        polygon = PolygonVisual(vertices=vertices, parent=self.view.scene)
        self.shapes.append(polygon)


if __name__ == '__main__':
    canvas = Canvas()
    canvas.add_circle(center=(0, 0), radius=20)
    canvas.add_polygon(vertices=np.array([[30, 30], [50, 60], [70, 30]]))
    app.run()
