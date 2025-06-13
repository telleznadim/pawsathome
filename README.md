# 🐾 Paws at Home

## 📝 Nombre del proyecto

**Paws at Home**

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

## 🛠️ ¿Qué encontrarás en el repositorio?

1. Aplicaciones Django:
   - `accounts`: gestión de usuarios, perfiles y avatares.
   - `petsitting`: modelos, vistas y formularios para mascotas, cuidadores y solicitudes.
2. Plantillas HTML organizadas por funciones (listas, formularios, detalles).
3. Tailwind CSS para estilos visuales modernos.
4. Configuración de media y static para imágenes (avatares, mascotas, fotos de cuidadores).

---

## 📌 Enlace de vista previa

Puedes usar la versión _preview_ activa durante los próximos 7 días en:  
**[https://pawsathome.life/](https://pawsathome.life/)**

---
