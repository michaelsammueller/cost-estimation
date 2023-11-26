'''
    Includes all classes and methods for the cost estimator
'''
from data import json_data

# Classes
class ProjectEstimator:
    '''
    The Project Estimator class is used to estimate the cost of a software
    engineering project. It is able to create "HardwareComponent", "SoftwareComponent",
    and "StaffMember" objects and add them to the estimator. It can then calculate
    the total cost of the system, the cost per system, and estimate the staffing cost for
    the software using the COCOMO model.
    '''
    def __init__(self):
        # Empty dictionaries that will host individual objects.
        self.software_components = {}
        self.hardware_components = {}
        self.resources = {}

    # Methods to add components and/or staff members to the estimator.
    # These methods are called by the read_json_data method. This allows
    # the Estimator to be populated with data, allowing other methods to
    # iterate over the information required to perform calculations.

    def clear(self):
        """clear"""
        self.software_components = {}
        self.hardware_components = {}
        self.resources = {}
    
    def store_initial_days(self):
        '''Stores the initial working days of staff members.'''
        self.initial_days = {staff_id: staff['Days'] for staff_id, staff in self.resources.items()}
    
    def reset_days_to_initial(self):
        '''Reset the "Days" value of staff members to the initial value.'''
        for staff_id, initial_days in self.initial_days.items():
            self.resources[staff_id]['Days'] = initial_days

    def add_software_component(self, software_component):
        '''Adds software component to software component dictionary.'''
        # Filter out None values from the skills as not all components require 3 skills
        required_skills = [skill for skill
                           in [software_component.skill_1_needed,
                               software_component.skill_2_needed,
                               software_component.skill_3_needed]
                               if skill is not None]
        self.software_components[software_component.description] = {
            "Count": software_component.count,
            "Cost": (software_component.price * 1000), # per quantity of 1000
            "Manufacturing Cost": software_component.manufacturing_cost,
            "Design Cost": software_component.design_cost,
            "Coding Cost": software_component.coding_cost,
            "Testing Cost": software_component.testing_cost,
            "Lines of Code": software_component.lines_of_code,
            "Skills Required": required_skills
        }

    def add_hardware_component(self, hardware_component):
        '''Adds hardware component to hardware component dictionary.'''
        # Filter out None values from the skills as not all components require 3 skills
        required_skills = [skill for skill
                           in [hardware_component.skill_1_needed,
                               hardware_component.skill_2_needed,
                               hardware_component.skill_3_needed]
                               if skill is not None]
        self.hardware_components[hardware_component.description] = {
            "Count": hardware_component.count,
            "Cost": (hardware_component.price * 1000), # per quantity of 1000
            "Manufacturing Cost": (hardware_component.manufacturing_cost * 1000),
            "Design Cost": hardware_component.design_cost,
            "Coding Cost": hardware_component.coding_cost,
            "Testing Cost": hardware_component.testing_cost,
            "Skills Required": required_skills
        }

    def add_staff_member(self, staff_member):
        '''Adds staff member to staff member dictionary.'''
        # Filter out None values from the skills as not all staff members have 3 skills
        skills = [skill for skill
                  in [staff_member.skill_1,
                      staff_member.skill_2,
                      staff_member.skill_3]
                      if skill is not None]
        staff_id = (staff_member.role + " - " + staff_member.type)
        self.resources[staff_id] = {
            "Count": staff_member.count,
            "Cost": staff_member.cost,
            "Days": staff_member.days,
            "Skills": skills
        }

    # Methods to calculate costs:
    # - Total Software Cost - Calculates the cost of all software components.
    # - Total Hardware Cost - Calculates the cost of all hardware components.
    # - Total Design Cost - Calculates the cost of all design work.
    # - Total Manufacturing Cost - Calculates the cost of all manufacturing work.
    # - Total Coding Cost - Calculates the cost of all coding work.
    # - Total Testing Cost - Calculates the cost of all testing work.
    # - Total System Cost - Calculates the total cost of all 2000 systems.
    # - Cost per System - Calculates the cost per system.
    # - COCOMO Estimation - Estimates the cost of the system using the COCOMO model.

    def total_software_cost(self):
        '''Calculate the cost of all software components in GBP.'''
        total_cost = 0
        for component in self.software_components:
            total_cost += (self.software_components[component]['Cost']
                           * self.software_components[component]['Count'])
        return total_cost

    def total_hardware_cost(self):
        '''Calculate the cost of all hardware components in GBP.'''
        total_cost = 0
        for component in self.hardware_components:
            total_cost += (self.hardware_components[component]['Cost']
                           * self.hardware_components[component]['Count'])
        return total_cost

    def total_design_cost(self):
        '''Calculate the cost of all design work in GBP.'''
        total_cost = 0
        work_cap = 260 # Maximum number of days a staff member can work

        # Merge hardware and software into single list of tuples
        all_components = [(name, details) for name, details in self.hardware_components.items()] + [(name, details) for name, details in self.software_components.items()]

        # Step 1: Filter components that require design skills
        design_components = [component for component in all_components
                             if 'hardware design' in component[1]['Skills Required'] or
                             'software design' in component[1]['Skills Required']]

        # Step 2: Filter staff with design skills and sort by cost
        design_staff = sorted([staff for staff in self.resources.values()
                               if 'hardware design' in staff['Skills'] or
                               'software design' in staff['Skills']],
                               key=lambda x: x['Cost'])

        # Step 3: Assign components to staff
        for name, component in design_components:
            component_assigned = False
            for required_skill in component['Skills Required']:
                for staff in design_staff:
                    if not component_assigned and required_skill in staff['Skills'] and staff['Days'] + component['Design Cost'] <= work_cap:
                        staff['Days'] += component['Design Cost']
                        total_cost += staff['Cost'] * component['Design Cost']
                        component_assigned = True
                        break
                if component_assigned:
                    break
        # print(design_staff)
        return total_cost

    def total_manufacturing_cost(self):
        '''Calculate the cost of all manufacturing cost in GBP.'''
        total_cost = 0
        for component in self.hardware_components:
            total_cost += (self.hardware_components[component]['Manufacturing Cost']
                           * self.hardware_components[component]['Count'])
        return total_cost


    def total_coding_cost(self):
        '''Calculate the cost of all coding work in GBP.'''
        total_cost = 0
        work_cap = 260 # Maximum number of days a staff member can work

        # Add software components to list of tuples
        software_components = [(name, details) for name, details in self.software_components.items()]

        # Step 1: Filter components that require coding skills
        coding_components = [component for component in software_components
                                if 'code' in component[1]['Skills Required']]

        # Step 2: Filter staff with coding skills and sort by cost
        coding_staff = sorted([staff for staff in self.resources.values()
                                if 'code' in staff['Skills']],
                                key=lambda x: x['Cost'])

        # Step 3: Assign components to staff
        for name, component in coding_components:
            component_assigned = False
            for required_skill in component['Skills Required']:
                for staff in coding_staff:
                    if not component_assigned and required_skill in staff['Skills'] and staff['Days'] + component['Coding Cost'] <= work_cap:
                        staff['Days'] += component['Coding Cost']
                        total_cost += staff['Cost'] * component['Coding Cost'] * component['Count']
                        component_assigned = True
                        break
                if component_assigned:
                    break
        return total_cost

    def total_testing_cost(self):
        '''Calculate the cost of all testing work in GBP.'''
        total_cost = 0
        work_cap = 260 # Maximum number of days a staff member can work

        # Merge hardware and software into single list of tuples
        all_components = [(name, details) for name, details in self.hardware_components.items()] + [(name, details) for name, details in self.software_components.items()]

        # Step 1: Filter components that require testing skills
        testing_components = [component for component in all_components
                                if 'test' in component[1]['Skills Required']]

        # Step 2: Filter staff with testing skills and sort by cost
        testing_staff = sorted([staff for staff in self.resources.values()
                                if 'test' in staff['Skills']],
                                key=lambda x: x['Cost'])

        # Step 3: Assign components to staff
        for name, component in testing_components:
            component_assigned = False
            for required_skill in component['Skills Required']:
                for staff in testing_staff:
                    if not component_assigned and required_skill in staff['Skills'] and staff['Days'] + component['Testing Cost'] <= work_cap:
                        staff['Days'] += component['Testing Cost']
                        total_cost += staff['Cost'] * component['Testing Cost'] * component['Count']
                        component_assigned = True
                        break
                if component_assigned:
                    break
        return total_cost

    def total_system_cost(self):
        '''Calculate the total cost of the system in GBP.'''
        hardware_cost = self.total_hardware_cost()
        software_cost = self.total_software_cost()
        manufacturing_cost = self.total_manufacturing_cost()
        staff_cost = self.total_staff_cost()
        # Adding all individual costs together to calculate the cost of 1000 systems.
        # We then multiply by 2 to account for 2000 systems.
        return round(staff_cost + (hardware_cost * 2) + (software_cost * 2) + (manufacturing_cost * 2))

    def cost_per_system(self):
        '''Calculate the cost per system in GBP.'''
        # Divide the total system cost by 2000 to get the cost per system.
        return round(self.total_system_cost() / 2000)

    def total_staff_cost(self):
        """Calculate the total cost of all staff in GBP"""
        self.store_initial_days()
        total_cost = self.total_design_cost() + self.total_coding_cost() + self.total_testing_cost()
        self.reset_days_to_initial()

        return total_cost

    def cocomo_estimation(self, mode):
        '''Estimate the cost of the system using the COCOMO model.
        It takes a mode parameter which can be one of the following:
        - Organic
        - Semi-Detached
        - Embedded
        Based on the mode, the model will use the appropriate values for the
        effort multipliers and scale factors.'''

        # Creating constants we can access based on the mode.
        constants = {
            "Organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
            "Semi-Detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
            "Embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32}
        }

        # Step 1: Validate user input to avoid errors
        if mode in constants:
            a, b, c, d = constants[mode].values()
        else:
            raise ValueError("Invalid mode. Please use one of the following: Organic, Semi-Detached, Embedded")

        # Step 2: Iterate over all software components and calculate the total lines of code
        total_lines_of_code = 0
        for component in self.software_components:
            total_lines_of_code += (self.software_components[component]['Lines of Code']
                                    * self.software_components[component]['Count'])

        # Step 3: Calculate the scale factors
        # COCOMO II assigns values between 0.6 to 1.4 for each scale factor, with 1.0 being nominal.
        # We will assume that "moderate" is 1.0.
        #
        # Based on the case study for Synful, we will assume the following factors:
        # 1. Precedentedness - Moderate (Experience with indidivual components
        # but not building an entire system to this scale)
        # 2. Development Flexibility - Moderate (Some flexibility, but clear
        # requirements and a fixed deadline)
        # 3. Architecture/Risk Resolution - Low (Risks and their mtigations
        # have been identified)
        # 4. Team Cohesion - Low (Part of the team has worked together, some
        # are agency hires)
        # 5. Process Maturity - Moderate (Some processes are in place, but
        # new ones are being developed for this project)
        # 6. Required Software Reliability - Moderate (Consumer product, not
        # mission critical. Can be patched if bugs are found)

        scale_factor_values = {
            "Precedentedness": 1.0,
            "Development Flexibility": 1.0,
            "Architecture/Risk Resolution": 1.2,
            "Team Cohesion": 1.1,
            "Process Maturity": 1.0,
            "Required Software Reliability": 1.0
        }

        scale_factor = 1
        for value in scale_factor_values.values():
            scale_factor *= value

        # Step 4: Calculate the effort multipliers
        effort_multipliers = a * (total_lines_of_code / 1000) ** b * scale_factor
        development_time = c * (effort_multipliers ** d)
        # Check if development time is zero
        if development_time == 0:
            raise ValueError("Development time cannot be zero.")
        staff_required = effort_multipliers / development_time

        # Step 5: Estimate the cost of the system
        average_monthly_staff_cost = 6040 # Average monthly staff cost in GBP
        return round(average_monthly_staff_cost * staff_required * development_time)


    # Method to read data. This method is called to populate the CostEstimator class
    # with data from a JSON file. This method needs to be called first before any
    # calculations can be performed.
    # This method creates an instances of the HardwareComponent, SoftwareComponent,
    # and StaffMember classes and adds them to the relevant dictionaries in the
    # CostEstimator class.

    def read_json_data(self, json_data):
        '''Reads JSON data and adds it to the project estimator.'''
        for item in json_data['Hardware']:
            hardware_component = HardwareComponent(
                type=item['type'],
                description=item['description'],
                count=item['count'],
                price=item['price'],
                manufacturing_cost=item['manufacturing_cost'] * 5,
                design_cost=item['design_cost'] * 5,
                coding_cost=item['coding_cost'] * 5,
                testing_cost=item['testing_cost'] * 5,
                skill_1_needed=item.get('skill_1_needed', None),
                skill_2_needed=item.get('skill_2_needed', None),
                skill_3_needed=item.get('skill_3_needed', None)
            )
            self.add_hardware_component(hardware_component)

        for item in json_data['Software']:
            software_component = SoftwareComponent(
                type=item['type'],
                description=item['description'],
                count=item['count'],
                price=item['price'],
                manufacturing_cost=item['manufacturing_cost'] * 5,
                design_cost=item['design_cost'] * 5,
                coding_cost=item['coding_cost'] * 5,
                testing_cost=item['testing_cost'] * 5,
                lines_of_code=item['lines_of_code'],
                skill_1_needed=item.get('skill_1_needed', None),
                skill_2_needed=item.get('skill_2_needed', None),
                skill_3_needed=item.get('skill_3_needed', None)
            )
            self.add_software_component(software_component)

        for item in json_data['Resources']:
            staff_member = StaffMember(
                role=item['role'],
                type=item['type'],
                count=item['count'],
                cost=item['cost'],
                days=item['days'],
                skill_1=item.get('skill_1', None),
                skill_2=item.get('skill_2', None),
                skill_3=item.get('skill_3', None)
            )
            self.add_staff_member(staff_member)

class HardwareComponent:
    '''Class to represent a hardware component.'''
    def __init__(self, type, description, count, price, manufacturing_cost,
                 design_cost, coding_cost, testing_cost, skill_1_needed,
                 skill_2_needed, skill_3_needed):
        self.type = type
        self.description = description
        self.count = count
        self.price = price
        self.manufacturing_cost = manufacturing_cost
        self.design_cost = design_cost
        self.coding_cost = coding_cost
        self.testing_cost = testing_cost
        self.skill_1_needed = skill_1_needed
        self.skill_2_needed = skill_2_needed
        self.skill_3_needed = skill_3_needed

class SoftwareComponent:
    '''Class to represent a software component.'''
    def __init__(self, type, description, count, price, manufacturing_cost,
                 design_cost, coding_cost, testing_cost, lines_of_code,
                 skill_1_needed, skill_2_needed, skill_3_needed):
        self.type = type
        self.description = description
        self.count = count
        self.price = price
        self.manufacturing_cost = manufacturing_cost
        self.design_cost = design_cost
        self.coding_cost = coding_cost
        self.testing_cost = testing_cost
        self.lines_of_code = lines_of_code
        self.skill_1_needed = skill_1_needed
        self.skill_2_needed = skill_2_needed
        self.skill_3_needed = skill_3_needed

class StaffMember:
    '''Class to represent a staff member.'''
    def __init__(self, role, type, count, cost, days, skill_1, skill_2, skill_3):
        self.role = role
        self.type = type
        self.count = count
        self.cost = cost
        self.days = days # Duration assigned in days
        self.work_cap = 260 # Maximum number of days a staff member can work
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.skill_3 = skill_3

    def assign_to_task(self, days_required):
        '''Assigns staff member to a task for a given duration.'''
        if self.days + days_required <= self.work_cap:
            self.days += days_required
            return True
        return False

    def get_total_cost(self):
        '''Returns the cost for assigned duration.'''
        return self.cost * self.days

# Tests
pe = ProjectEstimator()
pe.read_json_data(json_data)
# print(f'Total System Cost (2000): {pe.total_system_cost()}')
# print(f'Cost per System: GBP {pe.cost_per_system()}')
# print(f'COCOCMO Estimation: GBP {pe.cocomo_estimation("Organic")}')
# print(f'Total Software Cost: GBP {pe.total_software_cost()}')
# print(f'Total Hardware Cost: GBP {pe.total_hardware_cost()}')
# print(f'Total Manufacturing Cost: GBP {pe.total_manufacturing_cost()}')
# print(f'Hardware Components: {pe.hardware_components}')
# print(f'Total Coding Cost: GBP {pe.total_coding_cost()}')
# print(pe.resources)
print(f'Total System Cost (2000): {pe.total_system_cost()}')
print(f'Total Cost per System: GBP {pe.cost_per_system()}')
print(f'Total Hardware Cost: GBP {pe.total_hardware_cost()}')
print(f'Total Software Cost: GBP {pe.total_software_cost()}')
print(f'Total Manufacturing Cost: GBP {pe.total_manufacturing_cost()}')
print(f'Total Staff Cost: GBP {pe.total_staff_cost()}')
print(f'Total Staff Cost per System: GBP {pe.total_staff_cost() / 2000}')
print(f'Total Manufacturing Cost per System: GBP {pe.total_manufacturing_cost() / 1000}')
print(f'Total Hardware Cost per System: GBP {pe.total_hardware_cost() / 1000}')
print(f'Total Software Cost per System: GBP {pe.total_software_cost() / 1000}')
