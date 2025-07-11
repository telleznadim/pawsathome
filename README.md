# 🐾 Paws at Home

## 📝 Nombre del proyecto

**Paws at Home**

![Banner del Proyecto](theme/static/images/readme_banner.jpg)

## 👨‍💻 Autores / Desarrolladores

- **Daniel Triana**
- **Nadim Tellez**

---

## 🎯 Objetivo funcional

Paws at Home es una plataforma web hecha con Django que conecta a **dueños de mascotas** con **cuidadores disponibles**. Permite:

- Registro y autenticación de usuarios como _Pet Owners_ o _Pet Sitters_
- Crear y gestionar perfiles detallados (foto, ciudad, experiencia, tarifa, etc.)
- Propietarios pueden registrar sus mascotas y contactar cuidadores
- Cuidadores reciben y gestionan solicitudes de trabajos (estado: pendiente, aceptado, rechazado, completado)
- Dueños pueden ver el historial de solicitudes enviadas

**Vista previa activa**: [https://pawsathome.life/](https://pawsathome.life/) (disponible en línea por 7 días)

---

## 🗂️ Modelos principales

### `CustomUser`

Hereda de `AbstractUser` y añade el campo:

- `user_type`: indica si el usuario es **owner** o **sitter**.

### `PetOwnerProfile`

Relaciona un `CustomUser` con datos adicionales:

- `user` (OneToOneField)
- `phone_number` y `address`

### `PetSitterProfile`

Perfil para cuidadores, incluye:

- `user` (OneToOneField)
- `bio`, `experience_years`, `hourly_rate`, `available`, `photo`, `city`

### `Pet` (en app `petsitting`)

Representa una mascota, con campos:

- `name`, `species`, `breed`, `age`, `notes`, `photo`
- `owner` (ForeignKey a `PetOwnerProfile`)

### `JobRequest`

Solicitudes de servicio entre dueño y cuidador, con:

- `owner`, `sitter`, `pets` (ManyToMany con `Pet`)
- `start_date`, `end_date`, `message`, `status`
- Campo de fecha `created_at`

---

## 📋 Requisitos del proyecto y cumplimiento

| Requisito                                                            | ¿Cumplido? | Descripción                                                                              |
| -------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------- |
| 1. Diseño/Template no usado en clase con 4 opciones de menú          | ✅ Sí      | Menú superior con: Inicio, Mascotas, Cuidadores, Login/Register, y más                   |
| 2. Login / Logout / Registro / Modificación de usuarios (con avatar) | ✅ Sí      | Login, Logout, Registro con selección de tipo (owner/sitter) y carga de imagen de perfil |
| 3. CRUD de al menos 4 modelos, solo para usuarios logueados          | ✅ Sí      | CRUD completo para: Pet, PetOwnerProfile, PetSitterProfile y JobRequest                  |
| 4. Página “Acerca de mí” con información del alumno                  | ✅ Sí      | Se encuentra en el sitio como página estática (about.html)                               |
| 5. Filtro de búsqueda (opcional)                                     | ✅ Sí      | Filtro de cuidadores por ciudad en la lista de Pet Sitters                               |

---

## 🧪 Resultados de pruebas unitarias

Puedes revisar los resultados de pruebas unitarias en el siguiente enlace de Google Drive:  
📁 [Ver resultados de pruebas](https://drive.google.com/drive/folders/1Y7wrpeScL7nyJEHFn_9VdWyKRbQVjitd?usp=drive_link)

---

## ▶️ Video explicativo del proyecto (próximamente)

🎥 [Ver en YouTube](https://youtu.be/THJDNn9FhaA)

---

## 📌 Enlace de vista previa

Puedes usar la versión _preview_ activa durante los próximos 7 días en:  
🌐 **[https://pawsathome.life/](https://pawsathome.life/)**

---

## 🛠️ Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/telleznadim/pawsathome.git
cd pawsathome
```

### 2. Crear y activar un entorno virtual

```bash
# En Linux o Mac
python -m venv env
source env/bin/activate

# En Windows
python -m venv env
env\Scripts\activate
```

### 3. Instalar las dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Instalar Tailwind CSS y dependencias de Node.js

```bash
cd theme
npm install
cd ..
```

### 5. Aplicar migraciones y ejecutar el servidor

```bash
python manage.py migrate
python manage.py runserver
Luego accede a: http://localhost:8000
```
