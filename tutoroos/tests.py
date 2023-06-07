from django.test import TestCase
from tutoroos.models import Course

# Create your tests here.
class DummyTest(TestCase):
    def test_is_a_true_dummy(self):
        self.assertIs(True, True)
        # self.factory = RequestFactory()

class TestCourseCreation(TestCase):
    def create_course(self):
        return Course.objects.create(mnemonic = "CS", course_number = "1110", course_name = "Intro")

    def test_course_creation(self):
        c = self.create_course()
        self.assertTrue(isinstance(c, Course))

    def test_course_mn(self):
        c = self.create_course()
        self.assertEqual(c.mnemonic, "CS")

    def test_course_num(self):
        c = self.create_course()
        self.assertEqual(c.course_number, "1110")

    def test_course_name(self):
        c = self.create_course()
        self.assertEqual(c.course_name, "Intro")

class Tutor(TestCase):
    def tutor_rating_neg(self):
        tutor = Tutor(
            data={'name': 'AJ', 'price': '100', 'subject': 'math', 'rating': '5', 'numRatings': '20'}
        )
        self.assertTrue(isinstance(tutor, Tutor))
