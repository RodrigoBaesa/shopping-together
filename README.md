#  ShoppingTogether: Collaborative Shopping & Dietary Safety


## Academic Context
This application was developed as the **Final Project** for **CS50x: Introduction to Computer Science** from **Harvard University**. It represents the culmination of the course, integrating concepts of low-level memory management (C), web development (Python/Flask), and data persistence (SQL). The project serves as a practical demonstration of my ability to design, implement, and deploy a full-stack solution to solve a real-world problem.

---

## Project Overview

**ShoppingTogether** is a collaborative web platform designed to solve the common chaos of household shopping. The project was born from the need to align brand preferences, item priorities, and, most importantly, ensure the **dietary safety** of family members with specific restrictions (such as lactose or gluten intolerance).

Unlike a standard shopping list, **ShoppingTogether** operates on a **Family Circles** logic. It manages not just *what* to buy, but *how* to buy according to each member's specific tastes and health needs.

-----

## Key Features

| Feature | Description |
| :--- | :--- |
| **Dynamic Groups** | Create a "Family Circle" and invite members via a unique code. |
| **Brand Preferences** | Click an item to see which brands your partner or roommate prefers. |
| **Dietary Safety Filter** | Automatic alerts if a product (e.g., "Milk") is added to a list with an intolerant member. |
| **Priority Levels** | Items categorized as `CRITICAL`, `RESTOCK`, or `WISHLIST`. |

---

## Security Implementation

As I have a keen interest in **Cybersecurity**, this project implements some safety layers:

>   * **Bcrypt Hashing:** No plain-text passwords.
>   * **SQL:** Protection against SQL Injection.
>   * **Session Integrity:** Secure cookie handling for user authentication.

---
