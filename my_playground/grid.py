import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk

class GridWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Grid Demo")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(central_widget)
        layout.addWidget(self.vtk_widget)

        # Set up the renderer
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer.SetBackground(0.1, 0.1, 0.1)  # Dark gray background

        # Set up unit transform
        self.transform = vtk.vtkTransform()
        self.transform.Scale(2.54, 2.54, 2.54)  # Convert inches to cm
        
        # Create the grid
        self.create_grid()
        
        # Create origin dot
        self.create_origin_dot()

        # Set up camera
        self.setup_camera()

        # Initialize the interactor
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()

    def create_grid(self):
        # Create grid lines (5 lines in each direction, 10cm apart)
        grid_size = 4  # Size in inches
        spacing = 4     # 4 inches spacing

        for i in range(-grid_size, grid_size + spacing, spacing):
            for j in range(-grid_size, grid_size + spacing, spacing):
                # Create X lines (along X-axis)
                line_x = vtk.vtkLineSource()
                line_x.SetPoint1(i, j, -grid_size)
                line_x.SetPoint2(i, j, grid_size)

                # Apply transform
                transformFilter_x = vtk.vtkTransformPolyDataFilter()
                transformFilter_x.SetInputConnection(line_x.GetOutputPort())
                transformFilter_x.SetTransform(self.transform)

                mapper_x = vtk.vtkPolyDataMapper()
                mapper_x.SetInputConnection(transformFilter_x.GetOutputPort())

                actor_x = vtk.vtkActor()
                actor_x.SetMapper(mapper_x)
                actor_x.GetProperty().SetColor(0.5, 0.5, 0.5)
                self.renderer.AddActor(actor_x)

                # Create Y lines (along Y-axis)
                line_y = vtk.vtkLineSource()
                line_y.SetPoint1(-grid_size, i, j)
                line_y.SetPoint2(grid_size, i, j)

                transformFilter_y = vtk.vtkTransformPolyDataFilter()
                transformFilter_y.SetInputConnection(line_y.GetOutputPort())
                transformFilter_y.SetTransform(self.transform)

                mapper_y = vtk.vtkPolyDataMapper()
                mapper_y.SetInputConnection(transformFilter_y.GetOutputPort())

                actor_y = vtk.vtkActor()
                actor_y.SetMapper(mapper_y)
                actor_y.GetProperty().SetColor(0.5, 0.5, 0.5)
                self.renderer.AddActor(actor_y)

                # Create Z lines (along Z-axis)
                line_z = vtk.vtkLineSource()
                line_z.SetPoint1(i, -grid_size, j)
                line_z.SetPoint2(i, grid_size, j)

                transformFilter_z = vtk.vtkTransformPolyDataFilter()
                transformFilter_z.SetInputConnection(line_z.GetOutputPort())
                transformFilter_z.SetTransform(self.transform)

                mapper_z = vtk.vtkPolyDataMapper()
                mapper_z.SetInputConnection(transformFilter_z.GetOutputPort())

                actor_z = vtk.vtkActor()
                actor_z.SetMapper(mapper_z)
                actor_z.GetProperty().SetColor(0.5, 0.5, 0.5)
                self.renderer.AddActor(actor_z)

        # Add 3-inch reference line
        line_3inch = vtk.vtkLineSource()
        line_3inch.SetPoint1(0, 0, 0)
        line_3inch.SetPoint2(3, 0, 0)  # 3 inches along X axis

        # Apply transform to reference line
        transformFilter_ref = vtk.vtkTransformPolyDataFilter()
        transformFilter_ref.SetInputConnection(line_3inch.GetOutputPort())
        transformFilter_ref.SetTransform(self.transform)

        mapper_3inch = vtk.vtkPolyDataMapper()
        mapper_3inch.SetInputConnection(transformFilter_ref.GetOutputPort())

        actor_3inch = vtk.vtkActor()
        actor_3inch.SetMapper(mapper_3inch)
        actor_3inch.GetProperty().SetColor(1.0, 1.0, 0.0)
        actor_3inch.GetProperty().SetLineWidth(3)
        self.renderer.AddActor(actor_3inch)

        # Add coordinate axes (also transformed)
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(8, 8, 8)  # Length in inches
        transform_axes = vtk.vtkTransform()
        transform_axes.Scale(2.54, 2.54, 2.54)
        axes.SetUserTransform(transform_axes)
        self.renderer.AddActor(axes)

    def create_origin_dot(self):
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(0, 0, 0)
        sphere.SetRadius(0.5)  # Radius in inches

        # Apply transform to sphere
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputConnection(sphere.GetOutputPort())
        transformFilter.SetTransform(self.transform)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transformFilter.GetOutputPort())

        self.origin_actor = vtk.vtkActor()
        self.origin_actor.SetMapper(mapper)
        self.origin_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        
        self.renderer.AddActor(self.origin_actor)

    def setup_camera(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(100, 100, 100)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        self.renderer.ResetCamera()

def main():
    app = QApplication(sys.argv)
    window = GridWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
