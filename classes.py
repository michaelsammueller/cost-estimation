"""
    Includes all classes and methods for the cost estimator
"""

class ProjectEstimator:
    def __init__(self):
        self.software_components = {}
        self.hardware_components = {}
        self.project_staff = {}
        self.design_tasks = {}
        self.manufacturing_tasks = {}
    
    def add_software_component(self, software_component):
        """Adds software component to software component dictionary."""
        pass

    def add_hardware_component(self, hardware_component):
        """Adds hardware component to hardware component dictionary."""
        pass

    def add_staff_member(self, staff_member):
        """Adds staff member to project staff dictionary."""
        pass

    def total_software_cost(self, software_components):
        """Calculates the total software cost."""
        total_cost = 0
        for component, cost in software_components:
            total_cost += cost
        
        return total_cost

    def total_hardware_cost(self, hardware_components):
        """Calculates the total hardware cost."""
        total_cost = 0
        for component, cost in hardware_components:
            total_cost += cost
        
        return total_cost

    def total_design_cost(self):
        pass

    def total_manufacturing_cost(self):
        pass

    def total_staff_cost(self):
        """Calculates total staff cost based
        on the cost of individual staff members
        and duration of assignment."""
        total_cost = 0
        for staff, cost in self.project_staff:
            total_cost += cost

        return total_cost
            
    def total_project_cost(self):
        """Calculates the total cost of the project."""

        pass

    def write_to_json(self, path):
        """Writes cost estimation to JSON file."""
        pass

    def read_json(self, path):
        """Reads cost estimation from JSON file."""
        pass

class HardwareComponent:
    def __init__(self, name, cost, design_weeks, manufacturing_weeks):
        self.name = name
        self.cost = cost
        self.design_weeks = design_weeks  # Weeks needed to design the component
        self.manufacturing_weeks = manufacturing_weeks  # Weeks needed to manufacture the component

class SoftwareComponent:
    def __init__(self, name, cost, design_weeks):
        self.name = name
        self.cost = cost
        self.design_weeks = design_weeks  # Weeks needed to manufacture the component

class StaffMember:
    def __init__(self, title, cost_per_day, employment_type, weeks_assigned):
        self.title = title  # Job Title
        self.cost_per_day = cost_per_day
        self.employment_type = employment_type  # In-House or Agency
        self.weeks_assigned = weeks_assigned  # Amount of weeks assigned to the job
        self.cost = (cost_per_day * 7) * weeks_assigned
    
    def get_cost(self):
        """Returns the cost for assigned duration"""
        return self.cost


# Temporary Tests
pe = ProjectEstimator()
hwa = StaffMember("Hardware Architect", 250, "In-House", 20)

pe.add_staff_member(hwa)

