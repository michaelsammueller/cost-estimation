"""
    Includes all classes and methods for the cost estimator
"""

class ProjectEstimator:
    def __init__(self):
        self.software_components = {}
        self.hardware_components = {}
        self.project_staff = {}
    
    def add_software_component(self, software_component):
        """Adds software component to software component dictionary."""
        self.software_components[software_component.name] = {
            "Cost": software_component.cost,
            "Design Weeks": software_component.design_weeks
        }

    def add_hardware_component(self, hardware_component):
        """Adds hardware component to hardware component dictionary."""
        self.hardware_components[hardware_component.name] = {
            "Cost": hardware_component.cost,
            "Design Weeks": hardware_component.design_weeks,
            "Manufacturing Weeks": hardware_component.manufacturing_weeks
        }

    def add_staff_member(self, staff_member):
        """Adds staff member to project staff dictionary."""
        self.project_staff[staff_member.title] = {
            "Daily Cost": staff_member.cost_per_day,
            "Employment Type": staff_member.employment_type,
            "Weeks Assigned": staff_member.weeks_assigned,
            "Total Cost": staff_member.get_total_cost()
        }

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
        """Calculates the total cost of the design
        in person-weeks."""
        total_weeks = 0
        for software in self.software_components.values():
            total_weeks += software["Design Weeks"]
        
        for hardware in self.hardware_components.values():
            total_weeks += hardware["Design Weeks"]
        
        return total_weeks

    def total_manufacturing_cost(self):
        """Calculates the total cost of manufacturing
        in person-weeks."""
        total_weeks = 0
        for hardware in self.hardware_components.values():
            total_weeks += hardware["Manufacturing Weeks"]
        
        return total_weeks

    def total_staff_cost(self):
        """Calculates total staff cost based
        on the cost of individual staff members
        and duration of assignment."""
        total_cost = 0
        for staff_member in self.project_staff.values():
            total_cost += staff_member["Total Cost"]

        return total_cost
            
    def total_project_cost(self):
        """Calculates the total monetary cost of the project,
        including staff cost, hardware cost, and software cost."""
        total_cost = 0
        for staff_member in self.project_staff.values():
            total_cost += staff_member["Total Cost"]
        
        for component in self.hardware_components.values():
            total_cost += component["Cost"]
        
        for component in self.software_components.values():
            total_cost += component["Cost"]
        
        return total_cost

    def write_to_json(self, path):
        """Writes cost estimation to JSON file."""
        pass

    def read_json(self, path):
        """Reads cost estimation from JSON file."""
        pass

class HardwareComponent:
    def __init__(self, name, cost, design_weeks, manufacturing_weeks):
        self.name = name
        self.cost = cost * 1000  # Cost per quantity thousand
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
        self.total_cost = (cost_per_day * 7) * weeks_assigned
    
    def get_total_cost(self):
        """Returns the cost for assigned duration"""
        return self.total_cost


# Temporary Tests
pe = ProjectEstimator()
hwa = StaffMember("Hardware Architect", 250, "In-House", 20)
swa = StaffMember("Software Architect", 450, "Agency", 20)
synful_kernel = SoftwareComponent("Synful Kernel", 0, 2)
cpu1 = HardwareComponent("68k0", 8, 0, 0)
board_sldr = HardwareComponent("A83", 15, 8, 10)


pe.add_staff_member(hwa)
pe.add_staff_member(swa)
pe.add_software_component(synful_kernel)
pe.add_hardware_component(cpu1)
pe.add_hardware_component(board_sldr)

print(f"Project Staff: {pe.project_staff}")
print(f"Software Components: {pe.software_components}")
print(f"Hardware Components: {pe.hardware_components}")

print(f"Total Staff Cost (GBP): {pe.total_staff_cost()}")
print(f"Total Design Cost (Person-Weeks): {pe.total_design_cost()}")
print(f"Total Manufacturing Cost (Person-Weeks): {pe.total_manufacturing_cost()}")
print(f"Total Estimated Project Cost (GBP): {pe.total_project_cost()}")
