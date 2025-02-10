import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from trakstar_interface import *  # Replace with your TrakSTARInterface import



class ReceiverTracker(QMainWindow):
    def __init__(self, trakstar, enable_origin_reset=True, use_origin=True):
        super().__init__()
        self.trakstar = trakstar
        self.enable_origin_reset = enable_origin_reset
        self.use_origin = use_origin

        # Add reference plane related attributes
        self.reference_points = []
        self.collecting_reference = False
        self.reference_timer = QTimer()
        self.reference_timer.timeout.connect(self.capture_reference_point)
        self.transform_matrix = None
        self.reference_origin = None

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

        # Add reset origin button only if enabled
        if self.enable_origin_reset:
            self.reset_origin_button = QPushButton("Reset Origin", self)
            self.reset_origin_button.clicked.connect(self.reset_origin)
            layout.addWidget(self.reset_origin_button)

        # Add reference plane button
        self.ref_plane_button = QPushButton("Set Reference Plane", self)
        self.ref_plane_button.clicked.connect(self.start_reference_collection)
        layout.addWidget(self.ref_plane_button)

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

        # Add origin-related attributes
        self.origin_set = False
        self.origin = None if self.use_origin else np.array([0, 0, 0])

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

    def start_reference_collection(self):
        """Start collecting reference points."""
        self.reference_points = []
        self.collecting_reference = True
        print("Starting reference plane collection...")
        print("Collecting point 1 of 3...")
        self.reference_timer.start(1000)  # Timer fires every 1 second

    def capture_reference_point(self):
        """Capture reference points."""
        if len(self.reference_points) >= 3:
            self.reference_timer.stop()
            self.collecting_reference = False
            self.create_transform_matrix()
            return

        data = self.trakstar.get_synchronous_data_dict(write_data_file=False)
        current_pos = np.array([val * 2.54 for val in data[1][:3]])
        self.reference_points.append(current_pos)
        print(f"Collected point {len(self.reference_points)} of 3...")
        
        if len(self.reference_points) == 3:
            self.reference_timer.stop()
            self.collecting_reference = False
            self.create_transform_matrix()

    def create_transform_matrix(self):
        """Create transformation matrix from reference points."""
        try:
            p1, p2, p3 = self.reference_points

            # Create vectors from points
            v1 = p2 - p1  # First vector
            v2 = p3 - p1  # Second vector
            
            # Calculate normal vector (new z-axis)
            z_new = np.cross(v1, v2)
            z_new = z_new / np.linalg.norm(z_new)
            
            # Calculate new x-axis (using v1 direction)
            x_new = v1 / np.linalg.norm(v1)
            
            # Calculate new y-axis (perpendicular to both z and x)
            y_new = np.cross(z_new, x_new)
            
            # Create rotation matrix
            self.transform_matrix = np.vstack([x_new, y_new, z_new]).T
            self.reference_origin = p1
            
            print("Reference plane successfully created!")
            print(f"Origin point: {self.reference_origin}")
            print(f"Transform matrix:\n{self.transform_matrix}")
        except Exception as e:
            print(f"Error creating transform matrix: {e}")
            self.transform_matrix = None
            self.reference_origin = None

    def transform_point(self, point):
        """Transform a point to the reference plane coordinate system."""
        if self.transform_matrix is None or self.reference_origin is None:
            return point
        return self.transform_matrix.T @ (point - self.reference_origin)

    def update_position(self):
        """Update position and render."""
        data = self.trakstar.get_synchronous_data_dict(write_data_file=False, unit="cm")
        current_pos = np.array(data[1][:3])  # No need for conversion here anymore

        # Set origin if using origin system and not set
        if self.use_origin and not self.origin_set:
            self.origin = current_pos
            self.origin_set = True
            print("Origin set at:", self.origin)
            return

        # Calculate position (either relative to origin or absolute)
        position = current_pos - (self.origin if self.use_origin else np.array([0, 0, 0]))
        
        # Transform position to reference plane coordinate system if available
        if self.transform_matrix is not None:
            position = self.transform_point(position)
        
        # Update display with position
        self.points.SetPoint(0, position[0], position[1], position[2])
        self.points.Modified()
        self.position_label.setText(f"X: {position[0]:.2f}, Y: {position[1]:.2f}, Z: {position[2]:.2f}")
        self.vtk_widget.GetRenderWindow().Render()

    def reset_origin(self):
        """Reset the origin to the current position."""
        if not self.enable_origin_reset:
            return
        self.origin_set = False
        self.origin = None
        print("Origin reset - next position will be new origin")


def main():
    trakstar = TrakSTARInterface()
    trakstar.initialize()
    app = QApplication(sys.argv)
    
    # Control both origin functionalities here
    enable_origin_reset = False  # Controls whether the reset button appears
    use_origin = False          # Controls whether to use origin system at all
    
    window = ReceiverTracker(trakstar, enable_origin_reset, use_origin)
    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()
