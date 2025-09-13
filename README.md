# 📘 LibreCourse

**LibreCourse** is a full-stack Django application designed for creating, organizing, and collaborating on courses.
It allows educators and learners to structure content into lessons, manage access, and engage in learning.

---

## 🚀 Features

* **User Management**

  * Custom user model (`CustomUser`) with authentication (signup/login).
  * Secure password handling and Django authentication framework integration.

* **Course Management**

  * Create, update, and manage courses.
  * Public, private, and draft visibility options.
  * Automatic timestamping for creation and updates.

* **Lessons**

  * Attach lessons to courses with ordered sequencing.
  * Automatic course update timestamps when lessons change.
  * Reorder lessons after creation for flexible structuring.

* **Tags**

  * Predefined tag system for categorizing courses.
  * Many-to-many relationship between courses and tags.

* **Collaboration**

  * Invite collaborators to co-manage courses.
  * Favorite courses feature for quick access.

* **Scalable Design**

  * Clean separation of apps (`users`, `courses`).
  * Ready for integration with Django REST Framework (API support).
  * Built with reusability and future expansion in mind.

---

## 🛠️ Tech Stack

* **Backend:** Django, Django ORM, Django Signals
* **Frontend (planned):** HTML, CSS, JavaScript (or React integration)
* **Database:** PostgreSQL
* **Other:** Django REST Framework, Bootstrap/Tailwind (UI flexibility)

---

✨ *LibreCourse is built to demonstrate clean Django architecture, scalability, and real-world feature planning.*

---

 This project is licensed under the GNU Affero General Public License version 3 (AGPLv3). View [LICENSE](LICENSE).
