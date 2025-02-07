import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from trakstar_interface import *  # Replace with your TrakSTARInterface import



class ReceiverTracker(QMainWindow):
    def __init__(self, trakstar):
        super().__init__()
        self.trakstar = trakstar

        # Set up the main window
        self.setWindowTitle("Receiver Position Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create the VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        layout.addWidget(self.vtk_widget)

        # Create a label for position text
        self.position_label = QLabel(self)
        self.position_label.setStyleSheet("font-size: 16px; color: white; background-color: rgba(0, 0, 0, 128);")
        self.position_label.setGeometry(10, 10, 300, 30)
        self.position_label.setText("X: 0.0, Y: 0.0, Z: 0.0")

        # Add button to set the reference plane
        self.set_reference_button = QPushButton("Set Reference Plane", self)
        self.set_reference_button.clicked.connect(self.start_reference_plane_mode)
        layout.addWidget(self.set_reference_button)

        # Create the VTK pipeline
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer.SetBackground(0.2, 0.2, 0.2)

        # Add coordinate axes
        axes_actor = self.create_axes(length=60.0)
        self.renderer.AddActor(axes_actor)

        # Initialize the interactor
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()

        # Add orientation cube
        self.add_orientation_cube()

        # Create receiver point
        self.points = vtk.vtkPoints()
        self.points.InsertNextPoint(0, 0, 0)

        # Create polydata
        self.polydata = vtk.vtkPolyData()
        self.polydata.SetPoints(self.points)

        # Create sphere glyph
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1.0)
        sphere.SetPhiResolution(20)
        sphere.SetThetaResolution(20)

        self.glyph = vtk.vtkGlyph3D()
        self.glyph.SetInputData(self.polydata)
        self.glyph.SetSourceConnection(sphere.GetOutputPort())
        self.glyph.ScalingOff()

        # Mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.glyph.GetOutputPort())

        self.point_actor = vtk.vtkActor()
        self.point_actor.SetMapper(mapper)
        self.point_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        self.renderer.AddActor(self.point_actor)

        # Timer for position updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)

        # Reference plane setup
        self.reference_plane = None
        self.reference_timer = QTimer()
        self.reference_timer.timeout.connect(self.capture_reference_point)
        self.reference_points = []
        self.reference_mode = False

    def create_axes(self, length=10.0):
        """Create coordinate system axes."""
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(length, length, length)
        axes.SetShaftTypeToLine()
        return axes

    def add_orientation_cube(self):
        """Add orientation cube."""
        cube = vtk.vtkAnnotatedCubeActor()
        cube.SetFaceTextScale(0.5)
        cube.SetXPlusFaceText("Right")
        cube.SetXMinusFaceText("Left")
        cube.SetYPlusFaceText("Up")
        cube.SetYMinusFaceText("Down")
        cube.SetZPlusFaceText("Front")
        cube.SetZMinusFaceText("Back")

        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(cube)
        widget.SetViewport(0.8, 0.0, 1.0, 0.2)
        widget.SetInteractor(self.iren)
        widget.EnabledOn()
        widget.InteractiveOn()

    def start_reference_plane_mode(self):
        """Start setting reference plane."""
        print("Begin waving on reference plane...")
        self.reference_points = []
        self.reference_mode = True
        self.reference_timer.start(50)
        QTimer.singleShot(1000, self.finish_reference_plane_mode)

    def capture_reference_point(self):
        """Capture reference points."""
        if self.reference_mode:
            data = self.trakstar.get_synchronous_data_dict(write_data_file=False)
            x, y, z = data[1][:3]
            self.reference_points.append(np.array([x, y, z]))

    def finish_reference_plane_mode(self):
        """Finish setting reference plane."""
        self.reference_mode = False
        self.reference_timer.stop()
        if len(self.reference_points) >= 3:
            self.reference_plane = self.compute_reference_plane(self.reference_points)
            print(f"Reference plane set: {self.reference_plane}")
        else:
            print("Not enough points for reference plane.")

    def compute_reference_plane(self, points):
        """Compute reference plane equation."""
        p1, p2, p3 = points[:3]
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        a, b, c = normal / np.linalg.norm(normal)
        d = -np.dot(normal, p1)
        return np.array([a, b, c, d])

    def adjust_to_reference_plane(self, x, y, z):
        """Adjust a point while preserving Z-movement."""
        if self.reference_plane is None:
            return np.array([x, y, z])
        a, b, c, d = self.reference_plane
        normal = np.array([a, b, c]) / np.linalg.norm([a, b, c])
        z_axis = np.array([0, 0, 1])
        v = np.cross(normal, z_axis)
        s = np.linalg.norm(v)
        c = np.dot(normal, z_axis)
        vx = np.array([
            [0, -v[2], v[1]],
            [v[2], 0, -v[0]],
            [-v[1], v[0], 0]
        ])
        rotation_matrix = np.eye(3) + vx + (vx @ vx) * ((1 - c) / (s**2)) if s != 0 else np.eye(3)
        point = np.array([x, y, z]) - (-d * normal)
        return rotation_matrix @ point

    def update_position(self):
        """Update position and render."""
        data = self.trakstar.get_synchronous_data_dict(write_data_file=False)
        x, y, z = data[1][:3]
        adjusted_position = self.adjust_to_reference_plane(x, y, z)
        self.points.SetPoint(0, adjusted_position[0], adjusted_position[1], adjusted_position[2])
        self.points.Modified()
        self.position_label.setText(f"X: {adjusted_position[0]:.2f}, Y: {adjusted_position[1]:.2f}, Z: {adjusted_position[2]:.2f}")
        self.vtk_widget.GetRenderWindow().Render()


def main():
    trakstar = TrakSTARInterface()
    trakstar.initialize()
    app = QApplication(sys.argv)
    window = ReceiverTracker(trakstar)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
