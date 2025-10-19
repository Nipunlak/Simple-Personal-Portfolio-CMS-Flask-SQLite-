# Personal Portfolio CMS (Flask + SQLite)

A simple content management system (CMS) built with **Flask**, **SQLite3**, and **Bootstrap**. This app lets users manage their own blog posts and portfolio projects with role-based access.

---

## Features

- 🧑‍💻 **User Authentication**  
  - Session-based login (no Flask-Login)  
  - Admins can register new users and assign roles

- 🔐 **Role-Based Access**  
  - Two roles: `Admin` and `User`  
  - Users can create, edit, and delete **their own** content  
  - Admins cannot edit others' content, only manage users

- 📝 **Content Management**  
  - Blog posts and portfolio projects with full CRUD  
  - Users can view all content but only modify their own

- 🖼️ **Image URL Support**  
  - Embed images via external URLs (no file upload)

---

## Roles and Permissions

| Role   | View All | Create | Edit/Delete Own | Edit/Delete Others | Register Users |
|--------|----------|--------|-----------------|--------------------|----------------|
| User   | ✅        | ✅      | ✅               | ❌                  | ❌             |
| Admin  | ✅        | ✅      | ✅               | ❌                  | ✅             |

---

## Tech Stack

- Flask (Python)  
- SQLite3  
- Bootstrap 5  
- Jinja2 templates  

---

## Planned Features

- Pagination for blog and projects  
- Search and filtering options  
- Optional file/image upload support  

---

## Getting Started

```bash
git clone https://github.com/yourusername/portfolio-cms.git
cd portfolio-cms

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
flask --app run run
