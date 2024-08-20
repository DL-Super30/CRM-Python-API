# Generated by Django 5.1 on 2024-08-19 09:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CreateNewLead",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("cc", models.BigIntegerField()),
                ("contact_no", models.BigIntegerField()),
                ("email", models.EmailField(max_length=255)),
                ("fee_coated", models.DecimalField(decimal_places=2, max_digits=10)),
                ("description", models.TextField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "lead_source",
                    models.CharField(
                        choices=[
                            ("None", "None"),
                            ("WalkIn", "WalkIn"),
                            ("StudentReferral", "StudentReferral"),
                            ("Demo", "Demo"),
                            ("WebSite", "WebSite"),
                            ("WebsiteChat", "WebsiteChat"),
                            ("InboundCall", "InboundCall"),
                            ("GoogleAdWords", "GoogleAdWords"),
                            ("FacebookAds", "FacebookAds"),
                            ("GoogleMyBusiness", "GoogleMyBusiness"),
                            ("WhatsAppDigitalLync", "WhatsAppDigitalLync"),
                        ],
                        default="None",
                        max_length=20,
                    ),
                ),
                (
                    "batch_timing",
                    models.CharField(
                        choices=[
                            ("7AM_8AM", "7AM_8AM"),
                            ("8AM_9AM", "8AM_9AM"),
                            ("9AM_10AM", "9AM_10AM"),
                            ("10AM_11AM", "10AM_11AM"),
                            ("11AM_12PM", "11AM_12PM"),
                            ("12PM_1PM", "12PM_1PM"),
                            ("1PM_2PM", "1PM_2PM"),
                            ("2PM_3PM", "2PM_3PM"),
                            ("3PM_4PM", "3PM_4PM"),
                            ("4PM_5PM", "4PM_5PM"),
                            ("5PM_6PM", "5PM_6PM"),
                            ("6PM_7PM", "6PM_7PM"),
                            ("7PM_8PM", "7PM_8PM"),
                            ("8PM_9PM", "8PM_9PM"),
                        ],
                        default="7AM_8AM",
                        max_length=10,
                    ),
                ),
                (
                    "class_mode",
                    models.CharField(
                        choices=[
                            ("HYDClassRoom", "HYDClassRoom"),
                            ("BLRClassRoom", "BLRClassRoom"),
                            ("IndiaOnline", "IndiaOnline"),
                            ("InternationalOnline", "InternationalOnline"),
                        ],
                        default="HYDClassRoom",
                        max_length=20,
                    ),
                ),
                (
                    "lead_status",
                    models.CharField(
                        choices=[
                            ("None", "None"),
                            ("NotContacted", "NotContacted"),
                            ("Attempted", "Attempted"),
                            ("WarmLead", "WarmLead"),
                            ("Opportunity", "Opportunity"),
                            ("AttendedDemo", "AttendedDemo"),
                            ("Visited", "Visited"),
                            ("Registered", "Registered"),
                            ("ColdLead", "ColdLead"),
                        ],
                        default="None",
                        max_length=12,
                    ),
                ),
                (
                    "courses",
                    models.CharField(
                        choices=[
                            ("Angulaar", "Angulaar"),
                            ("AWS", "AWS"),
                            ("AWSWithDevOps", "AWSWithDevOps"),
                            ("Azure", "Azure"),
                            ("AzureDevOps", "AzureDevOps"),
                            ("BusinessAnlayst", "BusinessAnlayst"),
                            ("CloudOpsMasters", "CloudOpsMasters"),
                            ("DevOps", "DevOps"),
                            ("FrontEndAngular", "FrontEndAngular"),
                            ("FrontEndReact", "FrontEndReact"),
                            ("FullStackJAVA", "FullStackJAVA"),
                            ("FullStackMEAN", "FullStackMEAN"),
                            ("FullStackMERN", "FullStackMERN"),
                            ("FullstackPython", "FullstackPython"),
                            ("FullStackReactJAVA", "FullStackReactJAVA"),
                            ("Java", "Java"),
                            ("NeedCounselling", "NeedCounselling"),
                            ("Others", "Others"),
                            ("PowerBI", "PowerBI"),
                            ("Python", "Python"),
                            ("React", "React"),
                            ("SalesForceAdmin", "SalesForceAdmin"),
                            ("SalesforceDeveloper", "SalesforceDeveloper"),
                            ("ServiceNow", "ServiceNow"),
                            ("AzureDataEngineer", "AzureDataEngineer"),
                            ("Tableau", "Tableau"),
                            ("Testing", "Testing"),
                        ],
                        default="Angulaar",
                        max_length=20,
                    ),
                ),
                (
                    "tech_stack",
                    models.CharField(
                        choices=[
                            ("CloudOps", "CloudOps"),
                            ("Salesforce", "Salesforce"),
                            ("FullStack", "FullStack"),
                            ("DataStack", "DataStack"),
                            ("ServiceNow", "ServiceNow"),
                            ("BusinessStack", "BusinessStack"),
                            ("CareerCounselling", "CareerCounselling"),
                        ],
                        default="CloudOps",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
