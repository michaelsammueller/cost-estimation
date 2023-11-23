'''
    Includes all classes and methods for the cost estimator
'''

# Test Data
# TODO: Remove test data

json_data = {'Hardware': [{'type': 'Board', 'description': 'A83-S', 'count': 1, 'price': 25, 'manufacturing_cost': 14, 'design_cost': 8, 'coding_cost': 0, 'testing_cost': 1.38, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test', 'skill_3_needed': 'build'}, {'type': 'CPU', 'description': '68k0', 'count': 1, 'price': 8, 'manufacturing_cost': 0, 'design_cost': 0, 'coding_cost': 0, 'testing_cost': 0}, {'type': 'Glue Chip', 'description': 'G1', 'count': 1, 'price': 5, 'manufacturing_cost': 0, 'design_cost': 16, 'coding_cost': 0, 'testing_cost': 2.76, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test'}, {'type': 'Glue Chip', 'description': 'G2', 'count': 1, 'price': 5, 'manufacturing_cost': 0, 'design_cost': 16, 'coding_cost': 0, 'testing_cost': 2.76, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test'}, {'type': 'Glue Chip', 'description': 'G3', 'count': 1, 'price': 5, 'manufacturing_cost': 0, 'design_cost': 16, 'coding_cost': 0, 'testing_cost': 2.76, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test'}, {'type': 'Glue Chip', 'description': 'G4', 'count': 1, 'price': 5, 'manufacturing_cost': 0, 'design_cost': 16, 'coding_cost': 0, 'testing_cost': 2.76, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test'}, {'type': 'RAM', 'description': '256KB', 'count': 2, 'price': 5, 'manufacturing_cost': 0, 'design_cost': 16, 'coding_cost': 0, 'testing_cost': 2.76, 'skill_1_needed': 'hardware design', 'skill_2_needed': 'test'}], 'Software': [{'type': 'OS', 'description': 'HB/OS in ROM', 'count': 1, 'price': 0, 'manufacturing_cost': 0, 'design_cost': 9, 'coding_cost': 8.85, 'testing_cost': 1.38, 'lines_of_code': 100, 'skill_1_needed': 'code', 'skill_2_needed': 'test', 'skill_3_needed': 'software design'}, {'type': 'OS', 'description': 'MccOS', 'count': 1, 'price': 0, 'manufacturing_cost': 0, 'design_cost': 2.25, 'coding_cost': 2.95, 'testing_cost': 0.15, 'lines_of_code': 100, 'skill_1_needed': 'code', 'skill_2_needed': 'test', 'skill_3_needed': 'software design'}, {'type': 'OS', 'description': 'Libraries and drivers', 'count': 1, 'price': 25, 'manufacturing_cost': 0, 'design_cost': 12.38, 'coding_cost': 19.18, 'testing_cost': 0.52, 'lines_of_code': 100, 'skill_1_needed': 'code', 'skill_2_needed': 'test', 'skill_3_needed': 'software design'}], 'Resources': [{'role': 'Software Architect', 'type': 'Internal', 'count': 1, 'cost': 250, 'days': 0, 'skill_1': 'software design', 'skill_2': 'fault finding', 'skill_3': 'layout'}, {'role': 'Software Architect', 'type': 'Agency', 'count': 1, 'cost': 400, 'days': 0, 'skill_1': 'software design', 'skill_2': 'fault finding', 'skill_3': 'layout'}, {'role': 'Hardware Architect', 'count': 1, 'type': 'Internal', 'cost': 300, 'days': 0, 'skill_1': 'hardware design', 'skill_2': 'fault finding', 'skill_3': 'layout'}, {'role': 'Hardware Architect', 'count': 1, 'type': 'Agency', 'cost': 450, 'days': 0, 'skill_1': 'hardware design', 'skill_2': 'fault finding', 'skill_3': 'coding'}, {'role': 'Software Engineer', 'type': 'Internal', 'count': 1, 'cost': 195, 'days': 0, 'skill_1': 'code', 'skill_2': 'test', 'skill_3': 'troubleshoot'}, {'role': 'Software Engineer', 'type': 'Agency', 'count': 1, 'cost': 295, 'days': 0, 'skill_1': 'code', 'skill_2': 'test', 'skill_3': 'troubleshoot'}, {'role': 'Hardware Engineer', 'type': 'Internal', 'count': 1, 'cost': 175, 'days': 0, 'skill_1': 'build', 'skill_2': 'test', 'skill_3': 'troubleshoot'}, {'role': 'Hardware Engineer', 'type': 'Agency', 'count': 1, 'cost': 275, 'days': 0, 'skill_1': 'build', 'skill_2': 'test', 'skill_3': 'troubleshoot'}, {'role': 'Project Manager', 'type': 'Internal', 'count': 1, 'cost': 275, 'days': 0, 'skill_1': 'plan', 'skill_2': 'manage', 'skill_3': 'cost'}, {'role': 'Project Manager', 'type': 'Agency', 'count': 1, 'cost': 450, 'days': 0, 'skill_1': 'plan', 'skill_2': 'manage', 'skill_3': 'cost'}, {'role': 'Project Analyst', 'type': 'Internal', 'count': 1, 'cost': 175, 'days': 0, 'skill_1': 'update', 'skill_2': 'replan', 'skill_3': 'resourcing'}, {'role': 'Project Analyst', 'type': 'Agency', 'count': 1, 'cost': 250, 'days': 0, 'skill_1': 'update', 'skill_2': 'replan', 'skill_3': 'resourcing'}]}
# End Test Data

# Classes
class ProjectEstimator:
    def __init__(self):
        self.software_components = {}
        self.hardware_components = {}
        self.resources = {}
    
    # Methods to add components to the estimator
    def add_software_component(self, software_component):
        '''Adds software component to software component dictionary.'''
        # Filter out None values from the skills
        required_skills = [skill for skill in [software_component.skill_1_needed, software_component.skill_2_needed, software_component.skill_3_needed] if skill is not None]
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
        # Filter out None values from the skills
        required_skills = [skill for skill in [hardware_component.skill_1_needed, hardware_component.skill_2_needed, hardware_component.skill_3_needed] if skill is not None]
        self.hardware_components[hardware_component.description] = {
            "Count": hardware_component.count,
            "Cost": (hardware_component.price * 1000), # per quantity of 1000
            "Manufacturing Cost": hardware_component.manufacturing_cost,
            "Design Cost": hardware_component.design_cost,
            "Coding Cost": hardware_component.coding_cost,
            "Testing Cost": hardware_component.testing_cost,
            "Skills Required": required_skills
        }
    
    def add_staff_member(self, staff_member):
        '''Adds staff member to staff member dictionary.'''
        # Filter out None values from the skills
        skills = [skill for skill in [staff_member.skill_1, staff_member.skill_2, staff_member.skill_3] if skill is not None]
        staff_id = (staff_member.role + " - " + staff_member.type)
        self.resources[staff_id] = {
            "Count": staff_member.count,
            "Cost": staff_member.cost,
            "Days": staff_member.days,
            "Skills": skills
        }
    
    # Methods to calculate costs
    def total_software_cost(self):
        '''Calculate the cost of all software components in GBP.'''
        total_cost = 0
        for component in self.software_components:
            total_cost += self.software_components[component]['Cost'] * self.software_components[component]['Count']
        return total_cost
    
    def total_hardware_cost(self):
        '''Calculate the cost of all hardware components in GBP.'''
        total_cost = 0
        for component in self.hardware_components:
            total_cost += self.hardware_components[component]['Cost'] * self.hardware_components[component]['Count']
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
                        # print(f'{staff} assigned to {component} for {component["Design Cost"]} days.')
                        staff['Days'] += component['Design Cost']
                        total_cost += staff['Cost'] * component['Design Cost']
                        component_assigned = True
                        break
                if component_assigned:
                    break
        # print(design_staff)
        return total_cost

    def total_manufacturing_cost(self):
        '''Calculate the cost of all manufacturing work in GBP.'''
        total_cost = 0
        work_cap = 260 # Maximum number of days a staff member can work

        # Add hardware components to list of tuples
        hardware_components = [(name, details) for name, details in self.hardware_components.items()]

        # Step 1: Filter components that require manufacturing skills
        manufacturing_components = [component for component in hardware_components
                                    if 'build' in component[1]['Skills Required']]
        
        # Step 2: Filter staff with manufacturing skills and sort by cost
        manufacturing_staff = sorted([staff for staff in self.resources.values()
                                      if 'build' in staff['Skills']],
                                      key=lambda x: x['Cost'])
        
        # Step 3: Assign components to staff
        for name, component in manufacturing_components:
            component_assigned = False
            for required_skill in component['Skills Required']:
                for staff in manufacturing_staff:
                    if not component_assigned and required_skill in staff['Skills'] and staff['Days'] + component['Manufacturing Cost'] <= work_cap:
                        # print(f'{staff} assigned to {component} for {component["Manufacturing Cost"]} days')
                        staff['Days'] += component['Manufacturing Cost']
                        total_cost += staff['Cost'] * component['Manufacturing Cost'] * component['Count']
                        component_assigned = True
                        break
                if component_assigned:
                    break
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
                        # print(f'{staff} assigned to {component} for {component["Coding Cost"]} days')
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
                        # print(f'{staff} assigned to {component} for {component["Testing Cost"]} days')
                        staff['Days'] += component['Testing Cost']
                        total_cost += staff['Cost'] * component['Testing Cost'] * component['Count']
                        component_assigned = True
                        break
                if component_assigned:
                    break
        return total_cost

    def total_system_cost(self):
        '''Calculate the total cost of the system in GBP.'''
        design_cost = self.total_design_cost()
        manufacturing_cost = self.total_manufacturing_cost()
        coding_cost = self.total_coding_cost()
        testing_cost = self.total_testing_cost()
        return (design_cost + manufacturing_cost + coding_cost + testing_cost) * 2
    
    def cost_per_system(self):
        '''Calculate the cost per system in GBP.'''
        return (self.total_system_cost() / 2000)
    
    def cocomo_estimation(self):
        '''Estimate the cost of the system using the COCOMO model.'''
        pass

    # Method to read data
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
    def __init__(self, type, description, count, price, manufacturing_cost, design_cost, coding_cost, testing_cost, skill_1_needed, skill_2_needed, skill_3_needed):
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
    def __init__(self, type, description, count, price, manufacturing_cost, design_cost, coding_cost, testing_cost, lines_of_code, skill_1_needed, skill_2_needed, skill_3_needed):
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
        else:
            return False

    def get_total_cost(self):
        '''Returns the cost for assigned duration.'''
        return self.cost * self.days

# Tests
pe = ProjectEstimator()
pe.read_json_data(json_data)
print(pe.total_system_cost())
print(pe.cost_per_system())
print(pe.resources)