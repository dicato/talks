autoscale: true
slidenumbers: true
theme: Business Class, 1

## Zero Downtime Migrations in Django
### _Ryan Scott_

---

# Introduction

- Software Engineer @ Percipient Networks
- Several years using Python and Django for fun
- 7 months using Python and Django professionally
- ~1 year using Python and Django professionally

---

# Topics

- What does zero downtime mean?
- What is a zero downtime deployment?
- What is a migration?
- How does Django query for data?
- How do you migrate without downtime?

---

![400%](website-under-construction.jpg)

---

# What does zero downtime mean?

- End-users can continue using the website without noticing anything
- All services remain functioning
- No downtime!

---

# Zero downtime deployments

- Without zero downtime deployments, zero downtime migrations are useless
- Many different methods to keep your Django app running while deploying changes:
  - Rolling deploy: Deploy to one web server at a time
  - Blue/green deploy: Stand up a duplicate set of web servers, swap them out after the deploy has finished

---

# What's a migration?

- Migrations allow Django to update the database schema from changes you've made to models.
- Migrations maintain a history of your database state.
- Migrations produce consistent results so that you can mirror development and production database state.

---

# Zero downtime migrations

- How do you make database changes without breaking Django?
- How do you keep your Django app running while changing the database?

---

# Example model

- A `Customer` represents a company with a name and a plan.

```python
class Customer(models.Model):
    company_name = models.CharField(max_length=32)
    plan = models.CharField(max_length=32)  # paid, free, etc.
```

---

# How does Django query for data?

- Django query:

```python
Customer.objects.all()
```

- Translates to this SQL query:

```sql
SELECT company_name, plan FROM customer;
```

- NOT:

```sql
SELECT * FROM customer;
```

---

# Leveraging Django's querying method

- Django only queries for fields that it knows about
- Fields can exist in the database without being defined in Django
- Django will raise an exception if a field is defined, but isn't in the database

---

# Migration Strategies

- Adding a field
- Adding a required field
- Removing a field

---

# Adding a field

- Add a new field for the company's address. The field *can* be blank.

```python
class Customer(models.Model):
    company_name = models.CharField(max_length=32)
    plan = models.CharField(max_length=32)  # paid, free, etc.
    company_address = models.CharField(blank=True, max_length=100)
```

---

# Adding a field

Steps to deploy the new field:

1. Migrate the database so that the new field exists.
2. Deploy your code to Django.

This ensures that the field exists in the database *before* Django starts using it.

---

# Adding a required field

- Adding a required field without a default is tricky because you have to backfill data.
- Django migrations support custom functions to backfill data that are run when the migration is applied.

```python
class Customer(models.Model):
    company_name = models.CharField(max_length=32)
    plan = models.CharField(max_length=32)  # paid, free, etc.
    company_address = models.CharField(blank=True, max_length=100)
    employee_count = models.IntegerField()  # This is required!
```

---

# Adding a required field (w/ RunPython)

1. Create your migration for the new field. Use a `RunPython` function in the migration file for backfilling data.
3. Migrate the database so that the new field exists and each row has the backfilled data.
4. Deploy your code to Django.

---

# Adding a required field (w/ RunPython)

- Using `RunPython` in migrations can be fragile, especially for large or complex data sets.
- If an exception is raised, Django will leave you in a weird state where it thinks the migration is complete when it really isn't.

---

# Adding a required field (w/ Mgmt Command)

- Management commands can be used as standalone scripts that interact with your database.
- Data migrations are a great use case for management commands.
- Design your command so that it migrates data in batches and can be run repeatedly.

---

# Adding a required field (w/ Mgmt Command)

- Use the `null=True` attribute to initially allow the field to be empty.

```python
class Customer(models.Model):
    company_name = models.CharField(max_length=32)
    plan = models.CharField(max_length=32)  # paid, free, etc.
    company_address = models.CharField(blank=True, max_length=100)
    employee_count = models.IntegerField(null=True)
```

---

# Adding a required field (w/ Mgmt Command)

1. Create a management command to backfill the data.
2. Migrate the database so the new field gets created (each row is `None`).
3. Deploy your code to Django and run the management command to backfill the data.
5. Remove the `null=True` attribute from the field and migrate the database again.
6. Deploy your code to Django.

---

# Removing a field

- Remove the plan field because we decided we don't need it

```python
class Customer(models.Model):
    company_name = models.CharField(max_length=32)
    # Removed plan field
    company_address = models.CharField(blank=True, max_length=100)
    employee_count = models.IntegerField(default=1)
```

---

# Removing a field

Steps to deploy the deleted field:

1. Deploy your code to Django.
2. Migrate the database so that the old field is deleted.

This ensures that Django stops using the field *before* it is deleted from the database.

---

# Complex migration strategies

- More complex migrations can be designed by building on these basic steps
- *Remember*: Understanding how Django queries for data will help you determine the order for migrating and deploying.
- Testing complex migrations:
[`github.com/plumdog/django_migration_testcase`](https://github.com/plumdog/django_migration_testcase)

---

# Thank you

## [github.com/percipient/talks](https://github.com/percipient/talks)
## ryan@strongarm.io
