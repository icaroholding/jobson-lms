import shutil
from pathlib import Path

import frappe
from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to

from lms.lms.api import give_discussions_permission


def after_install():
	create_batch_source()
	give_discussions_permission()


def after_sync():
	create_lms_roles()
	set_default_certificate_print_format()
	give_lms_roles_to_admin()
	override_frappe_logos()


def override_frappe_logos():
	"""Overwrite Frappe framework logo assets with the Jobson Academy logo.

	Runs on install and on every migrate so a `bench update` that restores
	the framework assets gets re-branded automatically.
	"""
	bench_path = Path(frappe.utils.get_bench_path())
	jobson_logo = bench_path / "sites/assets/lms/frontend/logo-jobson.png"
	frappe_images = bench_path / "sites/assets/frappe/images"

	if not jobson_logo.exists() or not frappe_images.is_dir():
		return

	for name in ("frappe-logo.png", "frappe-framework-logo.png"):
		target = frappe_images / name
		if target.exists():
			shutil.copy2(jobson_logo, target)

	svg_wrapper = (
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">'
		'<image href="/assets/lms/frontend/logo-jobson.png" width="500" height="500"/>'
		"</svg>"
	)
	for name in ("frappe-framework-logo.svg", "frappe-favicon.svg"):
		target = frappe_images / name
		if target.exists():
			target.write_text(svg_wrapper)


def before_uninstall():
	delete_custom_fields()
	delete_lms_roles()


def create_lms_roles():
	create_course_creator_role()
	create_moderator_role()
	create_evaluator_role()
	create_lms_student_role()


def delete_lms_roles():
	roles = ["Course Creator", "Moderator"]
	for role in roles:
		if frappe.db.exists("Role", role):
			frappe.db.delete("Role", role)


def create_course_creator_role():
	if frappe.db.exists("Role", "Course Creator"):
		frappe.db.set_value("Role", "Course Creator", "desk_access", 0)
	else:
		role = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": "Course Creator",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save()


def create_moderator_role():
	if frappe.db.exists("Role", "Moderator"):
		frappe.db.set_value("Role", "Moderator", "desk_access", 0)
	else:
		role = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": "Moderator",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save()


def create_evaluator_role():
	if frappe.db.exists("Role", "Batch Evaluator"):
		frappe.db.set_value("Role", "Batch Evaluator", "desk_access", 0)
	else:
		role = frappe.new_doc("Role")
		role.update(
			{
				"role_name": "Batch Evaluator",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save()


def create_lms_student_role():
	if frappe.db.exists("Role", "LMS Student"):
		frappe.db.set_value("Role", "LMS Student", "desk_access", 0)
	else:
		role = frappe.new_doc("Role")
		role.update(
			{
				"role_name": "LMS Student",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save()


def set_default_certificate_print_format():
	filters = {
		"doc_type": "LMS Certificate",
		"property": "default_print_format",
	}
	if not frappe.db.exists("Property Setter", filters):
		filters.update(
			{
				"doctype_or_field": "DocType",
				"property_type": "Data",
				"value": "Certificate",
			}
		)

		doc = frappe.new_doc("Property Setter")
		doc.update(filters)
		doc.save()


def delete_custom_fields():
	fields = [
		"user_category",
		"headline",
		"college",
		"city",
		"verify_terms",
		"country",
		"preferred_location",
		"preferred_functions",
		"preferred_industries",
		"work_environment_column",
		"time",
		"role",
		"carrer_preference_details",
		"skill",
		"certification_details",
		"internship",
		"branch",
		"github",
		"medium",
		"linkedin",
		"profession",
		"open_to",
		"cover_image" "work_environment",
		"dream_companies",
		"career_preference_column",
		"attire",
		"collaboration",
		"location_preference",
		"company_type",
		"skill_details",
		"certification",
		"education",
		"work_experience",
		"education_details",
		"hide_private",
		"work_experience_details",
		"profile_complete",
	]

	for field in fields:
		frappe.db.delete("Custom Field", {"fieldname": field})


def create_batch_source():
	sources = [
		"Newsletter",
		"LinkedIn",
		"Twitter",
		"Website",
		"Friend/Colleague/Connection",
		"Google Search",
	]

	for source in sources:
		if not frappe.db.exists("LMS Source", source):
			doc = frappe.new_doc("LMS Source")
			doc.source = source
			doc.save()


def give_lms_roles_to_admin():
	roles = ["Course Creator", "Moderator", "Batch Evaluator"]
	for role in roles:
		if not frappe.db.exists("Has Role", {"parent": "Administrator", "role": role}):
			doc = frappe.new_doc("Has Role")
			doc.parent = "Administrator"
			doc.parenttype = "User"
			doc.parentfield = "roles"
			doc.role = role
			doc.save()
