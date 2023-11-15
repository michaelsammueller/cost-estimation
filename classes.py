'''
    Includes all classes and methods for the cost estimator
'''

class ProjectEstimator:
    def __init__(self):
        self.software_components = {}
        self.hardware_components = {}
        self.project_staff = {}
    
    def add_software_component(self, software_component):
        '''Adds software component to software component dictionary.'''
        self.software_components[software_component.name] = {
            "Cost": software_component.cost,
            "Design Weeks": software_component.design_weeks,
            "Required Capabilities": software_component.required_capabilities
        }

    def add_hardware_component(self, hardware_component):
        '''Adds hardware component to hardware component dictionary.'''
        self.hardware_components[hardware_component.name] = {
            "Cost": hardware_component.cost,
            "Design Weeks": hardware_component.design_weeks,
            "Manufacturing Weeks": hardware_component.manufacturing_weeks,
            "Required Capabilities": hardware_component.required_capabilities
        }

    def add_staff_member(self, staff_member):
        '''Adds staff member to project staff dictionary.'''
        # Store the entire object in the dicitionary so we can access its attributes later
        self.project_staff[staff_member.title] = staff_member

    def total_software_cost(self, software_components):
        '''Calculates the total software cost.'''
        total_cost = 0
        for component, cost in software_components:
            total_cost += cost
        
        return total_cost

    def total_hardware_cost(self, hardware_components):
        '''Calculates the total hardware cost.'''
        total_cost = 0
        for component, cost in hardware_components:
            total_cost += cost
        
        return total_cost

    def total_design_cost(self):
        '''Calculates the total cost of the design
        in person-weeks.'''
        total_cost = 0
        # Looping over software components
        for component in self.software_components.values():
            # Convert design weeks to person days
            design_days = component['Design Weeks'] * 5
            # Allocate staff based on capabilities and available workday balance
            for capability in component['Required Capabilities']:
                for staff_title, staff in self.project_staff.items():
                    # Check whether any staff member has the required capability for the selected component
                    if capability in staff.capabilities and staff.assign_to_task(design_days):
                        total_cost += staff.get_total_cost()
                        break
        # Looping over hardware components
        for component in self.hardware_components.values():
            # Convert design weeks to person days
            design_days = component['Design Weeks'] * 5
            # Allcoate staff based on capabilities and available workday balance
            for capability in component['Required Capabilities']:
                for staff_title, staff in self.project_staff.items():
                    # Check whether any staff member has the required capability for the selected component
                    if capability in staff.capabilities and staff.assign_to_task(design_days):
                        total_cost += staff.get_total_cost()
                        break
        return total_cost

    def total_manufacturing_cost(self):
        '''Calculates the total cost of manufacturing
        in person-weeks.'''
        total_cost = 0
        for component in self.hardware_components.values():
            # Convert manufacturing weeks to person days
            manufacturing_days = component['Manufacturing Weeks'] * 5
            # Allocate staff based on capabilities and available workday balance
            for capability in component['Required Capabilities']:
                for staff_title, staff in self.project_staff.items():
                    # Check whether any staff member has the required capability for the selected component
                    if capability in staff.capabilities and staff.assign_to_task(manufacturing_days):
                        total_cost += staff.get_total_cost()
                        break
        return total_cost

    def total_staff_cost(self):
        '''Calculates total staff cost based
        on the cost of individual staff members
        and duration of assignment.'''
        total_cost = 0
        for staff_member in self.project_staff.values():
            total_cost += staff_member.get_total_cost()

        return total_cost
            
    def total_project_cost(self):
        '''Calculates the total monetary cost of the project,
        including staff cost, hardware cost, and software cost.'''
        total_cost = 0
        for staff_member in self.project_staff.values():
            total_cost += staff_member.get_total_cost()
        
        for component in self.hardware_components.values():
            total_cost += component["Cost"]
        
        for component in self.software_components.values():
            total_cost += component["Cost"]
        
        return total_cost
    
    def cocomo_estimation(self, loc, mode):
        '''Estimates the project cost using the
        COCOMO model. It accepts two arguments:
        1. loc = Lines of Code
        2. mode = Organic, Semi-Detached, or Embedded'''

        constants = {
            "Organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
            "Semi-Detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
            "Embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32},
        }

        # Validate user input to avoid error later
        if mode in constants:
            a, b, c, d = constants[mode].values()
        else:
            raise ValueError("Invalid mode selected. Please choose 'Organic', 'Semi-Detached', or 'Embedded'.")
        
        # Estimate cost using COCOMO formula
        effort = a * (loc/1000) ** b
        development_time = c * (effort**d)
        staff_required = effort/development_time

        # Average cost of GBP 6,040 per staff per month (Based on resources list)
        average_monthly_staff_cost = 6040

        # Calculate total cost
        total_cost = effort * average_monthly_staff_cost

        return total_cost

    def write_to_json(self, path):
        '''Writes cost estimation to JSON file.'''
        pass

    def read_json(self, path):
        '''Reads cost estimation from JSON file.'''
        pass

class HardwareComponent:
    def __init__(self, name, cost, design_weeks, manufacturing_weeks, capabilities):
        self.name = name
        self.cost = cost * 1000  # Cost per quantity thousand
        self.design_weeks = design_weeks  # Weeks needed to design the component
        self.manufacturing_weeks = manufacturing_weeks  # Weeks needed to manufacture the component
        self.required_capabilities = set(capabilities)

class SoftwareComponent:
    def __init__(self, name, cost, design_weeks, capabilities):
        self.name = name
        self.cost = cost
        self.design_weeks = design_weeks  # Weeks needed to manufacture the component
        self.required_capabilities = set(capabilities)

class StaffMember:
    def __init__(self, title, cost_per_day, employment_type, capabilities):
        self.title = title  # Job Title
        self.cost_per_day = cost_per_day
        self.employment_type = employment_type  # In-House or Agency
        self.workday_cap = 260  # Days
        self.capabilities = set(capabilities)
        self.workdays_used = 0
    
    def assign_to_task(self, days_required):
        '''Assigns staff member to a task for a specific number of days.'''
        # Use the counter object to check if enough days are available
        if self.workdays_used + days_required <= self.workday_cap:
            self.workdays_used += days_required
            return True
        return False
    
    def get_total_cost(self):
        '''Returns the cost for assigned duration'''
        return self.cost_per_day * self.workdays_used


# Temporary Tests
pe = ProjectEstimator()
hwa = StaffMember("Hardware Architect", 250, "In-House", ["Hardware Design", "Manufacture"])
swa = StaffMember("Software Architect", 450, "Agency", ["Software Design"])
synful_kernel = SoftwareComponent("Synful Kernel", 0, 2, ["Software Design"])
cpu1 = HardwareComponent("68k0", 8, 0, 0, ["Hardware Design"])
board_sldr = HardwareComponent("A83", 15, 8, 10, ["Hardware Design"])


pe.add_staff_member(hwa)
pe.add_staff_member(swa)
pe.add_software_component(synful_kernel)
pe.add_hardware_component(cpu1)
pe.add_hardware_component(board_sldr)
swa.assign_to_task(20)
hwa.assign_to_task(40)

print(f"Project Staff: {pe.project_staff}")
print(f"Software Components: {pe.software_components}")
print(f"Hardware Components: {pe.hardware_components}")

print(f"Estimated Total Staff Cost (GBP - COCOMO): {round(pe.cocomo_estimation(4000, 'Organic'))}")
print(f"Actual Total Staff Cost (GBP): {pe.total_staff_cost()}")
print(f"Total Design Cost (Person-Weeks): {pe.total_design_cost()}")
print(f"Total Manufacturing Cost (Person-Weeks): {pe.total_manufacturing_cost()}")
print(f"Actual Total Project Cost (GBP): {pe.total_project_cost()}")

