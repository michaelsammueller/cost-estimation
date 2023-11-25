
import unittest
from calculation import ProjectEstimator, HardwareComponent, SoftwareComponent, StaffMember

class TestProjectEstimator(unittest.TestCase):

    def setUp(self):
        self.pe = ProjectEstimator()

    def test_constructor(self):
        '''Test that the constructor creates a ProjectEstimator object'''
        self.assertIsInstance(self.pe, ProjectEstimator)

    def test_add_software_component(self):
        '''Test that a software component can be added to the project estimator'''
        software_component = SoftwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, 1000, "Skill1", "Skill2", "Skill3")
        self.pe.add_software_component(software_component)
        self.assertIn("Description1", self.pe.software_components)

    def test_add_hardware_component(self):
        '''Test that a hardware component can be added to the project estimator'''
        hardware_component = SoftwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, 1000, "Skill1", "Skill2", "Skill3")
        self.pe.add_hardware_component(hardware_component)
        self.assertIn("Description1", self.pe.hardware_components)

    def test_add_staff_member(self):
        '''Test that a staff member can be added to the project estimator'''
        staff_member = StaffMember("Developer", "Full-time", 5, 100, 10, "Coding", "Testing", None)
        self.pe.add_staff_member(staff_member)
        self.assertIn("Developer - Full-time", self.pe.resources)

    # Tests for calculation methods
    def test_total_software_cost(self):
        '''Test that the total software cost is calculated correctly'''
        software_component1 = SoftwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, 1000, "Skill1", "Skill2", "Skill3")
        software_component2 = SoftwareComponent("Type2", "Description2", 5, 15, 25, 35, 45, 55, 500, "Skill4", "Skill5", None)
        self.pe.add_software_component(software_component1)
        self.pe.add_software_component(software_component2)
        expected_cost = (20 * 10 + 15 * 5) * 1000  # (price * count) per 1000 units for each component
        self.assertEqual(self.pe.total_software_cost(), expected_cost)

    def test_total_hardware_cost(self):
        '''Test that the total hardware cost is calculated correctly'''
        hardware_component1 = HardwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, "Skill1", "Skill2", "Skill3")
        hardware_component2 = HardwareComponent("Type2", "Description2", 5, 15, 25, 35, 45, 55, "Skill4", "Skill5", None)
        self.pe.add_hardware_component(hardware_component1)
        self.pe.add_hardware_component(hardware_component2)
        expected_cost = (20 * 10 + 15 * 5) * 1000  # (price * count) per 1000 units for each component
        self.assertEqual(self.pe.total_hardware_cost(), expected_cost)

    def test_total_system_cost(self):
        '''Test that the total system cost is calculated correctly'''
        self.pe.add_software_component(SoftwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, 1000, "Skill1", "Skill2", "Skill3"))
        self.pe.add_hardware_component(HardwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, "Skill1", "Skill2", "Skill3"))
        total_cost = (self.pe.total_software_cost() + self.pe.total_hardware_cost() + self.pe.total_design_cost() + self.pe.total_manufacturing_cost() + self.pe.total_coding_cost() + self.pe.total_testing_cost()) * 2
        self.assertEqual(self.pe.total_system_cost(), total_cost)


class TestStaffMember(unittest.TestCase):

    def setUp(self):
        '''Test that the constructor creates a StaffMember object'''
        self.staff_member = StaffMember("Developer", "Full-time", 5, 100, 10, "Coding", "Testing", None)

    def test_assign_to_task(self):
        '''Test that a staff member can be assigned to a task'''
        result = self.staff_member.assign_to_task(20)
        self.assertTrue(result)
        self.assertEqual(self.staff_member.days, 30)

    def test_get_total_cost(self):
        '''Test that the total cost of a staff member is calculated correctly'''
        self.assertEqual(self.staff_member.get_total_cost(), 1000)

class TestSoftwareComponent(unittest.TestCase):

    def setUp(self):
        self.software_component = SoftwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, 1000, "Skill1", "Skill2", "Skill3")

    def test_constructor(self):
        '''Test that the constructor creates a SoftwareComponent object'''
        self.assertIsInstance(self.software_component, SoftwareComponent)

class TestHardwareComponent(unittest.TestCase):

    def setUp(self):
        self.hardware_component = HardwareComponent("Type1", "Description1", 10, 20, 30, 40, 50, 60, "Skill1", "Skill2", "Skill3")
    
    def test_constructor(self):
        '''Test that the constructor creates a HardwareComponent object'''
        self.assertIsInstance(self.hardware_component, HardwareComponent)

if __name__ == '__main__':
    unittest.main()
