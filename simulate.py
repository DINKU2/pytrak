import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
 
class ReceiverTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Receiver Position Tracker")
        self.setGeometry(100, 100, 800, 600)
       
        # Create the main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
       
        # Create the VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        layout.addWidget(self.vtk_widget)
       
        # Create the VTK pipeline
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
       
        # Set background color (dark gray)
        self.renderer.SetBackground(0.2, 0.2, 0.2)
       
        # Create coordinate axes
        axes_actor = self.create_axes()
        self.renderer.AddActor(axes_actor)
       
        # Create point for receiver position
        self.points = vtk.vtkPoints()
        self.points.InsertNextPoint(0, 0, 0)
       
        # Create polydata for point
        self.polydata = vtk.vtkPolyData()
        self.polydata.SetPoints(self.points)
       
        # Create sphere glyph
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(0.05)
        sphere.SetPhiResolution(20)
        sphere.SetThetaResolution(20)
       
        # Set up glyph
        self.glyph = vtk.vtkGlyph3D()
        self.glyph.SetInputData(self.polydata)
        self.glyph.SetSourceConnection(sphere.GetOutputPort())
        self.glyph.ScalingOff()
       
        # Create mapper and actor for point
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.glyph.GetOutputPort())
       
        self.point_actor = vtk.vtkActor()
        self.point_actor.SetMapper(mapper)
        self.point_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red color
       
        self.renderer.AddActor(self.point_actor)
       
        # Initialize camera
        self.renderer.ResetCamera()
        camera = self.renderer.GetActiveCamera()
        camera.Elevation(30)
        camera.Azimuth(30)
        camera.Zoom(0.8)
       
        # Initialize the interactor and start
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
       
        # Store origin and trail points
        self.origin = None
        self.trail_points = []
        self.trail_actor = None
       
    def create_axes(self):
        """Create coordinate system axes"""
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(1.0, 1.0, 1.0)
        axes.SetShaftTypeToLine()
       
        # Make the axes labels easier to read
        axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(12)
        axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(12)
        axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(12)
       
        return axes
       
    def update_position(self, x, y, z):
        """Update the receiver position and trail"""
        if self.origin is None:
            self.origin = np.array([x, y, z])
            position = np.array([0, 0, 0])
        else:
            position = np.array([x, y, z]) - self.origin
           
        # Update current position point
        self.points.SetPoint(0, position[0], position[1], position[2])
        self.points.Modified()
       
        # Update trail
        self.trail_points.append(position)
        if len(self.trail_points) > 100:  # Keep last 100 points
            self.trail_points.pop(0)
           
        # Update trail visualization
        self.update_trail()
       
        # Render
        self.vtk_widget.GetRenderWindow().Render()
       
    def update_trail(self):
        """Update the visualization of position trail"""
        if len(self.trail_points) < 2:
            return
           
        # Create points for trail
        points = vtk.vtkPoints()
        for point in self.trail_points:
            points.InsertNextPoint(point[0], point[1], point[2])
           
        # Create lines connecting points
        lines = vtk.vtkCellArray()
        for i in range(len(self.trail_points) - 1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i + 1)
            lines.InsertNextCell(line)
           
        # Create polydata for trail
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)
       
        # Create mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
       
        # Remove old trail actor if it exists
        if self.trail_actor is not None:
            self.renderer.RemoveActor(self.trail_actor)
           
        # Create new trail actor
        self.trail_actor = vtk.vtkActor()
        self.trail_actor.SetMapper(mapper)
        self.trail_actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # Light gray color
        self.trail_actor.GetProperty().SetLineWidth(2)
       
        self.renderer.AddActor(self.trail_actor)
 
def main():
    app = QApplication(sys.argv)
    window = ReceiverTracker()
    window.show()
   
    # Example: Update position periodically (replace with your actual position updates)
    from PyQt6.QtCore import QTimer
    timer = QTimer()
    t = [0]  # Using list to store mutable state
   
    def update():
        # Simulate circular movement
        x = np.cos(t[0])
        y = np.sin(t[0])
        z = np.sin(t[0]/2)
        window.update_position(x, y, z)
        t[0] += 0.1
   
    timer.timeout.connect(update)
    timer.start(25)  # Update every 100ms
   
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()