"""Unit tests for the upload functionality."""
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class UploadReportTest(TestCase):
    """Unit tests for uploading reports."""

    def setUp(self):
        """Create test user in database."""
        self.client = Client()

        self.test_user = "test1"
        self.test_email = "test1@example.com"
        self.test_pass = User.objects.make_random_password()
        self.user = User.objects.create_user(
            username=self.test_user, email=self.test_email, password=self.test_pass
        )
        self.assertTrue(
            self.client.login(username=self.test_user, password=self.test_pass)
        )

    def test_upload_pdf(self):
        """Test uploading .pdf file is successful."""
        # Simulate uploading a PDF file
        with open("./tests/testpdf.pdf", "rb") as file:
            response = self.client.post(
                reverse("report_upload"), {"file": file, "name": "Test Report"}
            )

        # If file is uploaded sucessfully, a redirect occurs
        self.assertEqual(response.status_code, 302)

    def test_upload_exe(self):
        """Test uploading exe is unsuccessful."""
        # Simulate uploading an EXE file
        with open("./tests/testexe.exe", "rb") as file:
            response = self.client.post(
                reverse("report_upload"), {"file": file, "name": "Test Report"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Only PDF and DOCX files are allowed.")

    def test_upload_no_name(self):
        """Test uploading file with no name is unsuccessful."""
        # Simulate uploading a PDF file
        with open("./tests/testpdf.pdf", "rb") as file:
            response = self.client.post(reverse("report_upload"), {"file": file})

        # If file is uploaded sucessfully, a redirect occurs
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_upload_exists(self):
        """Test uploading file multiple times is unsuccessful."""
        # Simulate uploading a PDF file
        with open("./tests/testpdf.pdf", "rb") as file:
            response = self.client.post(
                reverse("report_upload"), {"file": file, "name": "Test Report"}
            )

        # If file is uploaded sucessfully, a redirect occurs
        self.assertEqual(response.status_code, 302)

        # Simulate upload another pdf with the same name
        with open("./tests/testpdf.pdf", "rb") as file:
            response = self.client.post(
                reverse("report_upload"), {"file": file, "name": "Test Report"}
            )

        # If file is uploaded sucessfully, a redirect occurs, which is not expected for this case
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, "Report with this Name already exists")
