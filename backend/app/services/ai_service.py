import json
import logging
import re
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from app.config import settings
from app.services.prompt_templates import (
    REQUIREMENT_ANALYSIS_SYSTEM_PROMPT,
    SRS_SYSTEM_PROMPT,
    UML_SYSTEM_PROMPT,
    DB_DESIGN_SYSTEM_PROMPT,
)

logger = logging.getLogger("ai_service")

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = None
        if self.api_key and self.api_key.strip():
            try:
                self.client = AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=settings.OPENAI_API_BASE
                )
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")

    async def _call_llm(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Call OpenAI LLM if configured; return parsed JSON dictionary."""
        if not self.client:
            return None
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content:
                cleaned = re.sub(r"^```(?:json)?\s*", "", content.strip())
                cleaned = re.sub(r"\s*```$", "", cleaned)
                return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}. Falling back to intelligent heuristic engine.")
        return None

    def _extract_domain_entities(self, title: str, description: str, domain: str = "") -> Dict[str, Any]:
        """Extract domain concepts, actors, and workflows from any arbitrary user project."""
        text = f"{title} {description}"
        stopwords = {
            "the", "and", "for", "with", "that", "this", "from", "are", "can", "will", "all",
            "has", "have", "had", "not", "but", "about", "into", "over", "after", "system",
            "app", "application", "platform", "management", "service", "software", "solution",
            "tool", "features", "allows", "users", "user", "create", "manage", "view", "track",
            "process", "online", "cloud", "based", "digital", "automated", "web", "mobile",
            "real", "time", "high", "scale", "simple", "complete", "intelligent", "efficient",
            "provide", "helps", "built", "designed", "including", "etc", "such", "hub", "portal"
        }

        words = re.findall(r'[A-Za-z]{3,}', text)
        
        actor_keywords = {
            "student": "Student", "learner": "Learner", "patient": "Patient", "doctor": "Physician",
            "member": "Member", "customer": "Customer", "shopper": "Shopper", "client": "Client",
            "driver": "Driver", "rider": "Rider", "passenger": "Passenger", "pilot": "Pilot",
            "owner": "Owner", "trainer": "Trainer", "instructor": "Instructor", "teacher": "Teacher",
            "librarian": "Librarian", "reader": "Reader", "borrower": "Borrower", "renter": "Renter",
            "guest": "Guest", "buyer": "Buyer", "seller": "Seller", "vendor": "Vendor", "merchant": "Merchant",
            "trader": "Trader", "investor": "Investor", "applicant": "Applicant", "donor": "Donor"
        }

        primary_actor = None
        for w in words:
            w_sing = w.lower()
            if w_sing.endswith('ies'): w_sing = w_sing[:-3] + 'y'
            elif w_sing.endswith('s') and not w_sing.endswith('ss'): w_sing = w_sing[:-1]
            
            if w_sing in actor_keywords:
                primary_actor = actor_keywords[w_sing]
                break

        title_words = [w.capitalize() for w in re.findall(r'[A-Za-z]{3,}', title) if w.lower() not in stopwords]
        if not primary_actor:
            prefix = title_words[0] if title_words else "Primary"
            primary_actor = f"{prefix} Member"

        admin_actor = f"{title_words[0] if title_words else 'System'} Administrator"

        candidates = []
        seen = set()
        for w in words:
            w_lower = w.lower()
            if w_lower not in stopwords and w_lower not in seen:
                seen.add(w_lower)
                if w.endswith("ies") and len(w) > 4:
                    sing = w[:-3].capitalize() + "y"
                elif w.endswith("s") and not w.endswith("ss") and len(w) > 3:
                    sing = w[:-1].capitalize()
                else:
                    sing = w.capitalize()
                if len(sing) > 2 and sing.lower() not in stopwords:
                    candidates.append(sing)

        forbidden = {"user", "admin", "administrator", "manager", "staff", "system", "platform", primary_actor.lower()}
        clean_entities = [c for c in candidates if c.lower() not in forbidden and c.capitalize() != primary_actor]
        
        e1 = clean_entities[0] if len(clean_entities) > 0 else (title_words[0] if title_words else "Item")
        e2 = clean_entities[1] if len(clean_entities) > 1 else "Transaction"
        e3 = clean_entities[2] if len(clean_entities) > 2 else "Schedule"
        e4 = clean_entities[3] if len(clean_entities) > 3 else "Record"

        return {
            "title": title,
            "primary_actor": primary_actor,
            "admin_actor": admin_actor,
            "e1": e1, "e2": e2, "e3": e3, "e4": e4
        }

    def _generate_heuristic_requirements(self, title: str, description: str, domain: str) -> Dict[str, Any]:
        """Intelligent heuristic generator for requirements analysis."""
        title_lower = title.lower()
        desc_lower = description.lower()
        dom_lower = (domain or "").lower()

        is_hospital = ("hosp" in title_lower or "clinic" in title_lower or "patient" in title_lower) and "pet" not in title_lower and "vet" not in title_lower
        is_lms = ("lms" in title_lower or "learning management" in title_lower) or ("course" in title_lower and "curriculum" in desc_lower)
        is_ecommerce = "e-commerce" in title_lower or "marketplace" in title_lower or "online store" in title_lower or "shopping cart" in desc_lower

        if is_hospital:
            return {
                "project_title": title,
                "summary": f"An enterprise-grade {title} designed to streamline clinical workflows, patient EHR management, doctor appointment scheduling, pharmacy inventory, and billing automation with strict HIPAA compliance.",
                "domain": "Healthcare & Clinical Informatics",
                "actors": [
                    {"name": "Patient", "type": "Primary", "description": "Registers, books outpatient appointments, views medical history, and pays invoices."},
                    {"name": "Physician / Doctor", "type": "Primary", "description": "Conducts consultations, issues electronic prescriptions (e-Rx), and logs clinical diagnoses."},
                    {"name": "Hospital Administrator", "type": "Secondary", "description": "Manages doctor schedules, ward/bed occupancy, audit logs, and system roles."},
                    {"name": "Pharmacist", "type": "Secondary", "description": "Dispenses prescribed medications, tracks batch inventory, and flags low stock."},
                    {"name": "Billing Officer", "type": "Secondary", "description": "Generates itemized invoices, processes insurance claims, and issues receipts."},
                    {"name": "HL7 / FHIR Integration Gateway", "type": "System", "description": "Integrates diagnostic laboratory machines and external PACS imaging servers."}
                ],
                "stakeholders": [
                    {"name": "Chief Medical Officer (CMO)", "interest": "Clinical efficiency, patient safety, and error reduction", "impact": "High"},
                    {"name": "Hospital Board & CFO", "interest": "Revenue cycle management and asset utilization", "impact": "High"},
                    {"name": "Patients & Caregivers", "interest": "Frictionless appointment booking and transparent billing", "impact": "High"},
                    {"name": "Compliance & Security Auditors", "interest": "HIPAA, GDPR, and NABH regulatory compliance", "impact": "High"}
                ],
                "functional_requirements": [
                    {
                        "id": "FR-01",
                        "category": "Patient Management",
                        "title": "Patient Registration and Electronic Health Record (EHR)",
                        "description": "The system shall create and maintain a unified digital patient profile containing demographics, allergies, medical history, and emergency contacts.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "System generates a unique National Health ID / Patient MRN upon registration.",
                            "Access to medical records is restricted by RBAC (Role-Based Access Control).",
                            "All EHR updates generate an immutable audit trail entry."
                        ]
                    },
                    {
                        "id": "FR-02",
                        "category": "Appointment Scheduling",
                        "title": "Real-time Doctor Slot Booking & Rescheduling",
                        "description": "Patients and reception staff shall view doctor availability calendars and book consultation slots with automated SMS/email reminders.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Overlapping bookings for the same doctor slot must be prevented atomically.",
                            "Cancellations before 2 hours trigger automatic slot release to waiting list.",
                            "Automated calendar sync via iCal and Webhooks."
                        ]
                    },
                    {
                        "id": "FR-03",
                        "category": "Clinical Consultation & E-Prescription",
                        "title": "Clinical Notes and E-Prescription (e-Rx)",
                        "description": "Physicians shall enter symptoms, ICD-10 diagnostic codes, and digital prescriptions with automated drug interaction alerts.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Prescriptions are transmitted digitally to the pharmacy module.",
                            "System checks drug-allergy interactions against patient record.",
                            "Supports digital signature verification."
                        ]
                    },
                    {
                        "id": "FR-04",
                        "category": "Pharmacy & Inventory",
                        "title": "Pharmacy Dispensation and Stock Replenishment",
                        "description": "Automated inventory decrement upon prescription fulfillment, batch expiry monitoring, and purchase order triggers.",
                        "priority": "Should Have",
                        "acceptance_criteria": [
                            "Stock decrement occurs synchronously upon barcode scan.",
                            "Alert sent to procurement manager when stock drops below minimum threshold."
                        ]
                    },
                    {
                        "id": "FR-05",
                        "category": "Billing & Insurance",
                        "title": "Multi-tier Invoicing and Insurance Claim Processing",
                        "description": "Consolidates room rent, laboratory tests, surgical fees, and pharmacy charges into a centralized invoice with third-party insurance claim submission.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Supports cash, card, payment gateway, and TPA insurance settlement.",
                            "Generates tax-compliant PDF invoices with digital watermark."
                        ]
                    }
                ],
                "non_functional_requirements": [
                    {"category": "Security", "metric": "Data Encryption & Access", "target": "AES-256 at rest, TLS 1.3 in transit, HIPAA & GDPR compliant."},
                    {"category": "Performance", "metric": "API Response Latency", "target": "p95 response time under 180ms for all clinical search operations."},
                    {"category": "Scalability", "metric": "Concurrent Users", "target": "Support 10,000 active concurrent sessions with zero degradation."},
                    {"category": "Reliability", "metric": "System Availability", "target": "99.99% annual uptime with automated active-passive database failover."},
                    {"category": "Usability", "metric": "Accessibility", "target": "WCAG 2.1 AA compliant UI accessible on desktop and tablet devices."}
                ],
                "scope": {
                    "in_scope": [
                        "Patient registration and demographic profiling",
                        "Outpatient and Inpatient appointment scheduling",
                        "Electronic Health Records (EHR) & e-Prescriptions",
                        "Pharmacy dispensing and basic inventory control",
                        "Itemized billing and payment receipts"
                    ],
                    "out_of_scope": [
                        "Autonomous surgical robotic interfacing",
                        "Clinical genomics deep-sequencing analysis",
                        "Custom on-premise hardware telemetry firmware"
                    ]
                }
            }

        elif is_lms:
            return {
                "project_title": title,
                "summary": f"A next-generation {title} enabling student enrollment, interactive lesson streaming, automated assignment grading, and verifiable certification.",
                "domain": "EdTech & Learning Management",
                "actors": [
                    {"name": "Student / Learner", "type": "Primary", "description": "Enrolls in courses, streams lecture videos, submits assignments, and tracks GPA."},
                    {"name": "Course Instructor", "type": "Primary", "description": "Publishes syllabus, uploads multimedia lessons, creates assignments, and grades submissions."},
                    {"name": "Academic Administrator", "type": "Secondary", "description": "Manages academic terms, course accreditation, student admissions, and faculty assignments."},
                    {"name": "Auto-Grading & Proctoring Gateway", "type": "System", "description": "Evaluates quiz attempts, runs automated code testing, and flags academic integrity violations."}
                ],
                "stakeholders": [
                    {"name": "University Dean / Educational Board", "interest": "Curriculum excellence, student retention, and accreditation standards", "impact": "High"},
                    {"name": "Instructors & Faculty", "interest": "Streamlined course delivery, grading automation, and student engagement", "impact": "High"},
                    {"name": "Students & Parents", "interest": "Intuitive learning portal, fair grading, and credential portability", "impact": "High"}
                ],
                "functional_requirements": [
                    {
                        "id": "FR-01",
                        "category": "Course Catalog & Lessons",
                        "title": "Hierarchical Course Curriculum & Video Lesson Delivery",
                        "description": "Instructors structure courses into modules, lessons, streaming video, downloadable PDFs, and supplementary reading materials.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Supports adaptive bitrate video streaming with bookmarking.",
                            "Lesson access controls enforce prerequisite module completion.",
                            "Content versioning tracks syllabus modifications."
                        ]
                    },
                    {
                        "id": "FR-02",
                        "category": "Enrollment & Progress",
                        "title": "Student Course Registration & Progress Tracking",
                        "description": "Students search course catalogs, enroll in open or gated courses, and monitor percentage completion via real-time progress bars.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Atomic enrollment transactions prevent class oversubscription.",
                            "Video watching progress persisted at 5-second intervals.",
                            "Automated email notifications for upcoming deadlines."
                        ]
                    },
                    {
                        "id": "FR-03",
                        "category": "Assignments & Grading",
                        "title": "Assignment Submission & Multi-format Grading Engine",
                        "description": "Students submit homework before due dates, and instructors assign numerical scores, rubrics, and line-item feedback.",
                        "priority": "Must Have",
                        "acceptance_criteria": [
                            "Enforces hard due-date cutoff with optional late penalty.",
                            "Supports automated MCQ grading and rubric-based manual grading.",
                            "Immutable gradebook logs with grade change audit history."
                        ]
                    },
                    {
                        "id": "FR-04",
                        "category": "Discussion & Forums",
                        "title": "Interactive Course Discussion Forums and Q&A",
                        "description": "Threaded discussion boards per course with upvoting, pinned instructor answers, and peer assignment review workflows.",
                        "priority": "Should Have",
                        "acceptance_criteria": [
                            "Threaded replies with markdown and LaTeX formula rendering.",
                            "Instructor replies highlighted with verified educator badge."
                        ]
                    },
                    {
                        "id": "FR-05",
                        "category": "Certificates & Verification",
                        "title": "Digital Course Completion Certificate Issuing",
                        "description": "Upon achieving passing threshold in all required lessons and exams, the system automatically generates a cryptographically signed PDF certificate.",
                        "priority": "Should Have",
                        "acceptance_criteria": [
                            "Generates unique verification QR code and public credential URL.",
                            "Prevents re-generation if course passing criteria are unmet."
                        ]
                    }
                ],
                "non_functional_requirements": [
                    {"category": "Performance", "metric": "Video Playback Latency", "target": "Initial video buffer start time < 800ms globally via CDN."},
                    {"category": "Scalability", "metric": "Exam Concurrency", "target": "Support 25,000 simultaneous students taking quizzes with zero data loss."},
                    {"category": "Security", "metric": "Data Privacy", "target": "FERPA & GDPR compliant student data isolation and encrypted storage."},
                    {"category": "Reliability", "metric": "Submission Durability", "target": "99.999% file durability on object storage with multi-region replication."},
                    {"category": "Usability", "metric": "Accessibility", "target": "WCAG 2.1 AA compliant with screen reader and closed-caption support."}
                ],
                "scope": {
                    "in_scope": [
                        "Course syllabus creation and lesson publishing",
                        "Student enrollment and progress tracking",
                        "Assignment submission and gradebook management",
                        "Automated quizzes and completion certificates"
                    ],
                    "out_of_scope": [
                        "On-campus physical dormitory room access control",
                        "University bookstore physical point-of-sale inventory"
                    ]
                }
            }

        elif is_ecommerce:
            return {
                "project_title": title,
                "summary": f"A scalable, multi-tenant {title} engineered for seamless product discovery, checkout conversion, vendor management, and automated fulfillment.",
                "domain": "E-Commerce & Digital Retail",
                "actors": [
                    {"name": "Customer / Shopper", "type": "Primary", "description": "Searches catalog, manages cart/wishlist, places orders, and tracks shipment."},
                    {"name": "Merchant / Vendor", "type": "Primary", "description": "Manages product catalog, prices, inventory levels, and fulfills customer orders."},
                    {"name": "Platform Administrator", "type": "Secondary", "description": "Oversees marketplace commissions, reviews disputes, and manages categories."},
                    {"name": "Payment Gateway (Stripe)", "type": "System", "description": "Processes PCI-DSS compliant credit card, Apple Pay, and digital wallet transactions."}
                ],
                "stakeholders": [
                    {"name": "Chief Commercial Officer", "interest": "Gross Merchandise Value (GMV), checkout conversion rate", "impact": "High"},
                    {"name": "Merchants & Vendors", "interest": "Inventory reconciliation, fast payouts, and low return rates", "impact": "High"},
                    {"name": "End Consumers", "interest": "Fast delivery, clear pricing, and hassle-free returns", "impact": "High"}
                ],
                "functional_requirements": [
                    {
                        "id": "FR-01",
                        "category": "Catalog & Search",
                        "title": "Faceted Product Search and Filter Indexing",
                        "description": "Users search products with autocomplete, multi-attribute facet filtering, price sorting, and instant stock indicators.",
                        "priority": "Must Have",
                        "acceptance_criteria": ["Sub-150ms search query response times.", "Real-time out-of-stock badges."]
                    },
                    {
                        "id": "FR-02",
                        "category": "Checkout & Payment",
                        "title": "Atomic Cart Checkout and Payment Processing",
                        "description": "Processes multi-item cart purchases, validates promotional discount coupons, and charges payment gateways idempotently.",
                        "priority": "Must Have",
                        "acceptance_criteria": ["Idempotency key prevents double billing on network retry.", "Inventory locked for 10 minutes during checkout."]
                    },
                    {
                        "id": "FR-03",
                        "category": "Order Management",
                        "title": "Vendor Order Fulfillment and Shipment Tracking",
                        "description": "Vendors generate packing slips, print shipping labels, and post tracking courier numbers for automated delivery notifications.",
                        "priority": "Must Have",
                        "acceptance_criteria": ["State transitions: PENDING -> PAID -> PROCESSING -> SHIPPED -> DELIVERED.", "Webhook notifications sent to buyer."]
                    }
                ],
                "non_functional_requirements": [
                    {"category": "Security", "metric": "Payment Compliance", "target": "PCI-DSS Level 1 certified tokenization, zero raw card storage."},
                    {"category": "Performance", "metric": "Checkout Latency", "target": "p99 checkout submission under 600ms under flash-sale load."},
                    {"category": "Scalability", "metric": "Black Friday Traffic", "target": "Auto-scale backend to handle 50,000 requests per second."}
                ],
                "scope": {
                    "in_scope": ["Product catalog, cart, checkout, payment gateway, order fulfillment"],
                    "out_of_scope": ["Custom physical warehouse robotics integration"]
                }
            }

        # Dynamic heuristic architecture for any arbitrary custom idea
        info = self._extract_domain_entities(title, description, domain)
        p_actor = info["primary_actor"]
        a_actor = info["admin_actor"]
        e1, e2, e3, e4 = info["e1"], info["e2"], info["e3"], info["e4"]

        return {
            "project_title": title,
            "summary": f"A scalable, cloud-native {title} engineered with micro-modular architecture, robust API contracts, and automated {e1} and {e2} management.",
            "domain": domain or "Software Architecture Solutions",
            "actors": [
                {"name": p_actor, "type": "Primary", "description": f"Interacts with core {title} services, creates {e1} entries, and initiates {e2} requests."},
                {"name": "Operations Manager", "type": "Secondary", "description": f"Monitors {e2} activity, reviews {e3} allocations, and handles operational workflows."},
                {"name": a_actor, "type": "Primary", "description": f"Manages platform configuration, tenant access, security audits, and role permissions."},
                {"name": "External Integration Gateway", "type": "System", "description": f"Handles webhooks, payment gateways, and background worker queues for {title}."}
            ],
            "stakeholders": [
                {"name": "Product Owner / Executive Sponsor", "interest": f"Operational efficiency, customer satisfaction, and {title} scalability", "impact": "High"},
                {"name": "Engineering & DevOps Team", "interest": "Maintainability, test coverage, and API reliability", "impact": "High"},
                {"name": "Security & Compliance Officer", "interest": "Data sovereignty, authentication standards, and encryption controls", "impact": "High"}
            ],
            "functional_requirements": [
                {
                    "id": "FR-01",
                    "category": f"{e1} Management",
                    "title": f"{e1} Registration and Lifecycle Tracking",
                    "description": f"The system shall provide capabilities to create, update, search, and manage {e1} records with validation.",
                    "priority": "Must Have",
                    "acceptance_criteria": [
                        f"System assigns a unique UUID identifier to each new {e1}.",
                        f"Status changes to {e1} trigger audit log entries."
                    ]
                },
                {
                    "id": "FR-02",
                    "category": f"{e2} Processing",
                    "title": f"Automated {e2} Execution Workflow",
                    "description": f"The system shall execute the principal {e2} business operations according to domain validation rules.",
                    "priority": "Must Have",
                    "acceptance_criteria": [
                        f"Transactions executed within atomic database boundaries.",
                        f"Successful {e2} triggers real-time event notification."
                    ]
                },
                {
                    "id": "FR-03",
                    "category": f"{e3} Coordination",
                    "title": f"{e3} Scheduling and Allocation Engine",
                    "description": f"Users and staff shall manage {e3} timelines, availability slots, and resource allocations without conflicts.",
                    "priority": "Should Have",
                    "acceptance_criteria": [
                        f"Prevents concurrent double-booking or slot conflicts.",
                        f"Supports automated reminders and rescheduling."
                    ]
                },
                {
                    "id": "FR-04",
                    "category": f"{e4} Auditing",
                    "title": f"{e4} History and Analytical Reporting",
                    "description": f"Aggregates performance metrics, generates {e4} logs, and renders operational dashboards.",
                    "priority": "Should Have",
                    "acceptance_criteria": [
                        "Provides exportable reports in CSV and JSON formats.",
                        "Filters logs by date range and actor ID."
                    ]
                },
                {
                    "id": "FR-05",
                    "category": "Notifications & Security",
                    "title": "OAuth2 Authentication and Multi-channel Notifications",
                    "description": "Provides secure JWT authorization and dispatches asynchronous notifications on key lifecycle events.",
                    "priority": "Must Have",
                    "acceptance_criteria": [
                        "Enforces role-based access control (RBAC).",
                        "Failed deliveries automatically retried with exponential backoff."
                    ]
                }
            ],
            "non_functional_requirements": [
                {"category": "Performance", "metric": "API Response Time", "target": "p95 latency under 200ms under standard operational load."},
                {"category": "Security", "metric": "Encryption & Transport", "target": "TLS 1.3 enforced, AES-256 for sensitive payload columns at rest."},
                {"category": "Scalability", "metric": "Concurrent Users", "target": "Support 10,000 active concurrent sessions with zero degradation."},
                {"category": "Reliability", "metric": "System Availability", "target": "99.9% annual uptime with automated health checks."},
                {"category": "Usability", "metric": "Accessibility", "target": "Responsive mobile and desktop UI conforming to WCAG 2.1 standards."}
            ],
            "scope": {
                "in_scope": [
                    f"{e1} creation, cataloging and status tracking",
                    f"{e2} processing and transactional workflows",
                    f"{e3} scheduling and resource allocation",
                    f"{e4} reporting, analytics and audit trails"
                ],
                "out_of_scope": [
                    "Legacy mainframe hardware synchronization",
                    "Custom on-device firmware telemetry flashing"
                ]
            }
        }

    def _generate_heuristic_srs(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Compile a complete IEEE 830-style SRS document."""
        frs = analysis.get("functional_requirements", [])
        nfrs = analysis.get("non_functional_requirements", [])
        actors = analysis.get("actors", [])

        primary_actor = actors[0]["name"] if actors else "User"

        use_cases = [
            {
                "id": "UC-01",
                "title": f"Authenticate and Access {title}",
                "actor": primary_actor,
                "trigger": f"{primary_actor} submits credentials on the login screen.",
                "preconditions": f"{primary_actor} account is registered and active.",
                "main_flow": [
                    "User navigates to login portal.",
                    "User enters registered email and secure password.",
                    "System validates credentials and verifies MFA token if configured.",
                    "System issues signed JWT session tokens.",
                    "User is redirected to the role-tailored dashboard."
                ],
                "alternative_flow": [
                    "3a. Invalid credentials: System displays error and increments failed attempt counter.",
                    "3b. 5 consecutive failed attempts: System temporarily locks account for 15 minutes."
                ],
                "postconditions": "Secure authenticated session established with valid bearer token."
            },
            {
                "id": "UC-02",
                "title": f"Execute Core Workflow for {title}",
                "actor": primary_actor,
                "trigger": f"{primary_actor} initiates a new business transaction.",
                "preconditions": "User is authenticated and possesses necessary role authorization.",
                "main_flow": [
                    "User requests creation or processing of domain entity.",
                    "System renders form with validated input fields.",
                    "User submits populated data.",
                    "System executes business logic validation and database commit.",
                    "System publishes confirmation event and returns success response."
                ],
                "alternative_flow": [
                    "4a. Validation error: System returns field-level error messages.",
                    "4b. Database lock timeout: System rolls back transaction and advises retry."
                ],
                "postconditions": "Entity persisted in PostgreSQL with audit log recorded."
            }
        ]

        md = f"""# Software Requirements Specification (SRS)
## {title}
**Version:** 1.0.0  
**Status:** Approved Architecture Draft  
**Standard:** IEEE Std 830-1998 / ISO/IEC/IEEE 29148  

---

## 1. Introduction
### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a complete technical specification for **{title}**. It outlines functional requirements, non-functional constraints, external interface definitions, and system behavior for developers, quality assurance teams, DevOps engineers, and project stakeholders.

### 1.2 Scope of the Software
{analysis.get('summary', description)}
The software will be deployed as a containerized web application consisting of a React frontend, FastAPI backend services, and a PostgreSQL relational database.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification
- **RBAC**: Role-Based Access Control
- **REST**: Representational State Transfer
- **JWT**: JSON Web Token
- **DDL**: Data Definition Language
- **p95/p99**: 95th/99th percentile response metrics

---

## 2. Overall Description
### 2.1 Product Perspective
The {title} is an autonomous, cloud-ready software application designed for high availability, security, and extensibility. It operates within a standard Docker containerized environment.

### 2.2 User Characteristics
The system accommodates several distinct actor classes:
"""
        for a in actors:
            md += f"- **{a.get('name')}** ({a.get('type')}): {a.get('description')}\n"

        md += """
---

## 3. Specific Requirements

### 3.1 Functional Requirements
"""
        for fr in frs:
            md += f"#### [{fr.get('id')}] {fr.get('title')}\n"
            md += f"- **Category:** {fr.get('category')}  \n"
            md += f"- **Priority:** {fr.get('priority')}  \n"
            md += f"- **Description:** {fr.get('description')}  \n"
            md += "- **Acceptance Criteria:**\n"
            for ac in fr.get("acceptance_criteria", []):
                md += f"  - {ac}\n"
            md += "\n"

        md += """### 3.2 Non-Functional Requirements
| Category | Metric / Standard | Target Specification |
|---|---|---|
"""
        for nfr in nfrs:
            md += f"| **{nfr.get('category')}** | {nfr.get('metric')} | {nfr.get('target')} |\n"

        md += """
---

## 4. Use Case Specifications
"""
        for uc in use_cases:
            md += f"### {uc['id']}: {uc['title']}\n"
            md += f"- **Primary Actor:** {uc['actor']}\n"
            md += f"- **Trigger:** {uc['trigger']}\n"
            md += f"- **Preconditions:** {uc['preconditions']}\n"
            md += "- **Main Success Scenario:**\n"
            for step in uc['main_flow']:
                md += f"  1. {step}\n"
            md += "- **Extensions / Alternative Flows:**\n"
            for step in uc['alternative_flow']:
                md += f"  - {step}\n"
            md += f"- **Postconditions:** {uc['postconditions']}\n\n"

        md += """---

## 5. Design Constraints & Assumptions
### 5.1 System Constraints
1. The backend application must run on Python 3.11+ using the FastAPI asynchronous framework.
2. The primary persistent data store must be PostgreSQL 15+.
3. All external client-server communications must be encrypted using TLS 1.3.
4. Containerization must adhere to Docker and OCI standards.

### 5.2 Assumptions & Dependencies
1. Network infrastructure supports WebSockets/HTTP/2 connections.
2. Database instances are provisioned with automated WAL (Write-Ahead Logging) backups.
3. Users utilize modern, standards-compliant web browsers (Chrome, Firefox, Safari, Edge).
"""

        return {
            "project_title": title,
            "version": "1.0.0",
            "introduction": f"This specification defines the system architecture, behavioral requirements, and data model for {title}.",
            "scope": analysis.get("summary", description),
            "objectives": [
                f"Automate end-to-end workflows for {title}.",
                "Deliver sub-200ms p95 API response times with horizontal scalability.",
                "Ensure robust data security, role-based access control, and regulatory compliance.",
                "Achieve 99.9% service availability with containerized resilience."
            ],
            "functional_requirements": frs,
            "non_functional_requirements": nfrs,
            "use_cases": use_cases,
            "constraints": [
                "PostgreSQL as primary ACID-compliant transactional datastore",
                "Python FastAPI backend with asynchronous request dispatch",
                "Frontend implemented in React with responsive design standards",
                "Deployment standardized via Docker and Docker Compose"
            ],
            "assumptions": [
                "Reliable persistent storage volumes for containerized database",
                "Standard HTTPS termination via reverse proxy / Nginx"
            ],
            "markdown_content": md
        }

    def _generate_heuristic_uml(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 5 syntactically valid Mermaid diagrams tailored to the domain."""
        title_lower = title.lower()
        desc_lower = description.lower()

        is_hospital = "hosp" in title_lower or "clinic" in title_lower or "health" in desc_lower or "patient" in desc_lower
        is_lms = "lms" in title_lower or "learn" in title_lower or "course" in title_lower or "student" in desc_lower or "school" in title_lower or "edtech" in title_lower or "teach" in desc_lower
        is_ecommerce = "shop" in title_lower or "store" in title_lower or "e-commerce" in title_lower or "marketplace" in title_lower or "cart" in desc_lower or "retail" in desc_lower

        if is_hospital:
            use_case = """graph LR
    subgraph Actors["System Actors"]
        Patient["Patient"]
        Doctor["Physician / Doctor"]
        Admin["Hospital Administrator"]
        Pharmacist["Pharmacist"]
    end

    subgraph CoreSystem["Hospital Management System Boundary"]
        UC1(["Register & Manage Profile"])
        UC2(["Book / Reschedule Appointment"])
        UC3(["Conduct Consultation & Log EHR"])
        UC4(["Issue Electronic Prescription"])
        UC5(["Dispense Medication & Manage Stock"])
        UC6(["Generate Bill & Settle Invoice"])
        UC7(["Manage Beds & Ward Allocations"])
    end

    Patient --> UC1
    Patient --> UC2
    Patient --> UC6
    Doctor --> UC3
    Doctor --> UC4
    Pharmacist --> UC5
    Admin --> UC7
    Admin --> UC1"""

            class_diag = """classDiagram
    class User {
        +UUID id
        +String email
        +String password_hash
        +String role
        +Timestamp created_at
        +login(credentials) Boolean
    }

    class Patient {
        +UUID patient_id
        +String mrn_number
        +String blood_group
        +String emergency_contact
        +getMedicalHistory() List
    }

    class Doctor {
        +UUID doctor_id
        +String specialization
        +String license_number
        +Decimal consultation_fee
        +getAvailability() Schedule
    }

    class Appointment {
        +UUID id
        +UUID patient_id
        +UUID doctor_id
        +DateTime scheduled_time
        +String status
        +reschedule(newTime) Boolean
        +cancel() Boolean
    }

    class MedicalRecord {
        +UUID id
        +UUID patient_id
        +UUID doctor_id
        +String diagnosis
        +String notes
        +DateTime visit_date
    }

    class Prescription {
        +UUID id
        +UUID record_id
        +String dosage_instructions
        +String status
        +fulfill() Boolean
    }

    class Invoice {
        +UUID id
        +UUID patient_id
        +Decimal total_amount
        +String payment_status
        +generateReceipt() PDF
    }

    User <|-- Patient
    User <|-- Doctor
    Patient "1" --> "*" Appointment : books
    Doctor "1" --> "*" Appointment : attends
    Patient "1" --> "*" MedicalRecord : has
    MedicalRecord "1" --> "1..*" Prescription : contains
    Patient "1" --> "*" Invoice : pays"""

            sequence_diag = """sequenceDiagram
    autonumber
    actor Patient
    participant Frontend as React Client
    participant Gateway as FastAPI Backend
    participant DB as PostgreSQL Database
    participant Notif as Notification Service

    Patient->>Frontend: Select Doctor & Preferred Time Slot
    Frontend->>Gateway: POST /api/appointments {doctorId, slotTime}
    Gateway->>DB: Check slot conflict & verify doctor availability
    alt Slot is Available
        DB-->>Gateway: Slot Confirmed
        Gateway->>DB: INSERT INTO appointments (status='BOOKED')
        DB-->>Gateway: Appointment Record Created
        Gateway-)Notif: Trigger SMS & Email confirmation event
        Gateway-->>Frontend: HTTP 201 Created {appointmentId, confirmation}
        Frontend-->>Patient: Display Booking Confirmation & Calendar Invite
    else Slot Already Booked
        DB-->>Gateway: Conflict Detected
        Gateway-->>Frontend: HTTP 409 Conflict (Slot unavailable)
        Frontend-->>Patient: Prompt to select alternative time slot
    end"""

            activity_diag = """flowchart TD
    Start([Patient Initiates Appointment]) --> CheckAuth{Is Patient Authenticated?}
    CheckAuth -- No --> Login[Redirect to Login / Registration]
    Login --> SelectDoc[Select Department & Doctor]
    CheckAuth -- Yes --> SelectDoc
    SelectDoc --> ViewCalendar[Fetch Available Slots]
    ViewCalendar --> PickSlot[Select Date and Time Slot]
    PickSlot --> CheckLock{Is Slot Temporarily Locked?}
    CheckLock -- Yes --> PickSlot
    CheckLock -- No --> LockSlot[Acquire 5-min Redis Lock on Slot]
    LockSlot --> ReviewSummary[Review Appointment Details]
    ReviewSummary --> ConfirmBooking[Confirm & Authorize]
    ConfirmBooking --> PersistDB[(Save Appointment to PostgreSQL)]
    PersistDB --> SendNotif[Dispatch Confirmation SMS/Email]
    SendNotif --> EndNode([Appointment Confirmed])"""

            component_diag = """flowchart TB
    subgraph ClientTier["Client Tier (Presentation Layer)"]
        WebSPA["React SPA (Web Browser)"]
        MobileWeb["Mobile Responsive PWA"]
    end

    subgraph APITier["Application & API Gateway Tier"]
        ReverseProxy["Nginx Reverse Proxy & SSL Termination"]
        FastAPIApp["FastAPI REST Backend Services"]
        AuthModule["OAuth2 / JWT Auth Engine"]
        ArchitectEngine["Software Architect Core Engine"]
    end

    subgraph DataTier["Data & Persistence Tier"]
        PostgresDB[("PostgreSQL 16 (Relational DB)")]
        RedisCache[("Redis (Session & Slot Locks)")]
    end

    subgraph ExternalTier["External Integrations"]
        SMSGateway["SMS & Email Dispatcher"]
        PaymentGateway["Payment Gateway (Stripe/Razorpay)"]
    end

    WebSPA -->|HTTPS / REST| ReverseProxy
    MobileWeb -->|HTTPS / REST| ReverseProxy
    ReverseProxy --> FastAPIApp
    FastAPIApp --> AuthModule
    FastAPIApp --> ArchitectEngine
    FastAPIApp -->|Async SQLAlchemy / asyncpg| PostgresDB
    FastAPIApp -->|Pub/Sub & Caching| RedisCache
    FastAPIApp -->|Webhooks & REST| SMSGateway
    FastAPIApp -->|Checkout API| PaymentGateway"""

        elif is_lms:
            use_case = """graph LR
    subgraph Actors["LMS Platform Actors"]
        Student["Student / Learner"]
        Instructor["Course Instructor"]
        Admin["Academic Administrator"]
    end

    subgraph CoreSystem["Learning Management System Boundary"]
        UC1(["Browse Course Catalog & Enroll"])
        UC2(["Watch Video Lessons & Read Notes"])
        UC3(["Submit Homework & Coding Assignments"])
        UC4(["Take Timed Quizzes & View Gradebook"])
        UC5(["Author Course Syllabus & Upload Media"])
        UC6(["Grade Submissions & Provide Feedback"])
        UC7(["Manage Student Rosters & Term Schedules"])
        UC8(["Generate Verified Completion Certificate"])
    end

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Instructor --> UC5
    Instructor --> UC6
    Admin --> UC7
    Admin --> UC8"""

            class_diag = """classDiagram
    class User {
        +UUID id
        +String email
        +String password_hash
        +String role
        +Timestamp created_at
        +login(credentials) Boolean
    }

    class Student {
        +UUID student_id
        +String student_number
        +getEnrolledCourses() List
        +getGpa() Decimal
    }

    class Instructor {
        +UUID instructor_id
        +String department
        +String bio
        +publishCourse(courseId) Boolean
    }

    class Course {
        +UUID id
        +UUID instructor_id
        +String title
        +String description
        +Decimal price
        +Boolean is_published
        +getLessons() List
    }

    class Lesson {
        +UUID id
        +UUID course_id
        +String title
        +String video_url
        +Integer order_index
        +markComplete(studentId) Boolean
    }

    class Enrollment {
        +UUID id
        +UUID student_id
        +UUID course_id
        +Decimal progress_percentage
        +DateTime enrolled_at
        +updateProgress() Decimal
    }

    class Assignment {
        +UUID id
        +UUID course_id
        +String title
        +DateTime due_date
        +Integer max_points
    }

    class Submission {
        +UUID id
        +UUID assignment_id
        +UUID student_id
        +String file_url
        +Integer score
        +DateTime submitted_at
        +grade(score, feedback) Boolean
    }

    User <|-- Student
    User <|-- Instructor
    Instructor "1" --> "*" Course : creates
    Course "1" --> "*" Lesson : contains
    Student "1" --> "*" Enrollment : enters
    Course "1" --> "*" Enrollment : accepts
    Course "1" --> "*" Assignment : assigns
    Student "1" --> "*" Submission : submits
    Assignment "1" --> "*" Submission : evaluates"""

            sequence_diag = """sequenceDiagram
    autonumber
    actor Student
    participant Client as React LMS Portal
    participant API as FastAPI Backend
    participant Storage as S3 File Storage
    participant DB as PostgreSQL Database
    participant AutoGrader as Auto-Grading Engine

    Student->>Client: Upload Assignment Solution (PDF / Code)
    Client->>API: POST /api/assignments/{id}/submit (Multipart Form)
    API->>Storage: Store solution file object
    Storage-->>API: S3 URL confirmed
    API->>DB: INSERT INTO submissions (assignment_id, student_id, file_url)
    DB-->>API: Submission persisted with timestamp
    API-)AutoGrader: Queue automated test verification
    AutoGrader->>DB: Record preliminary automated score
    API-->>Client: HTTP 201 Created (Submission Successful)
    Client-->>Student: Display "Submitted on Time" Receipt & Status"""

            activity_diag = """flowchart TD
    Start([Student Opens Course]) --> CheckEnrollment{Is Student Enrolled?}
    CheckEnrollment -- No --> ShowEnrollPrompt[Prompt Course Enrollment / Payment]
    ShowEnrollPrompt --> ProcessEnrollment[Persist Enrollment Record in DB]
    ProcessEnrollment --> LoadCurriculum[Load Course Lessons & Modules]
    CheckEnrollment -- Yes --> LoadCurriculum
    LoadCurriculum --> StreamLesson[Stream Video Lecture & Read Notes]
    StreamLesson --> MarkLessonDone[Update Student Progress Counter]
    MarkLessonDone --> HasQuiz{Does Module Have Quiz?}
    HasQuiz -- Yes --> TakeQuiz[Student Takes Timed Quiz]
    TakeQuiz --> CheckPass{Score >= 80%?}
    CheckPass -- No --> RetakePrompt[Review Material & Retake Quiz]
    RetakePrompt --> TakeQuiz
    CheckPass -- Yes --> CheckAllComplete{Are All Modules Completed?}
    HasQuiz -- No --> CheckAllComplete
    CheckAllComplete -- No --> LoadNextLesson[Load Next Lesson in Syllabus]
    LoadNextLesson --> StreamLesson
    CheckAllComplete -- Yes --> GenerateCert[Issue Verified Digital Certificate]
    GenerateCert --> EndNode([Course Completed Successfully])"""

            component_diag = """flowchart TB
    subgraph ClientLayer["Presentation Tier"]
        StudentSPA["Student Portal (React SPA)"]
        InstructorStudio["Instructor Authoring Studio"]
    end

    subgraph ServiceLayer["API & Application Gateway"]
        Nginx["Nginx Reverse Proxy & Static Cache"]
        FastAPIApp["FastAPI LMS REST API Services"]
        AuthModule["JWT & Role-Based Access Control"]
        WorkerQueue["Celery Background Worker (Auto-Grading)"]
    end

    subgraph StorageLayer["Data & Persistence Tier"]
        PostgresLMS[("PostgreSQL 16 (Courses, Enrollments, Grades)")]
        S3ObjectStore[("Cloud Object Storage (Lecture Videos & Submissions)")]
        RedisCache[("Redis (Active Quiz Sessions & Rate Limits)")]
    end

    StudentSPA -->|HTTPS / REST| Nginx
    InstructorStudio -->|HTTPS / REST| Nginx
    Nginx --> FastAPIApp
    FastAPIApp --> AuthModule
    FastAPIApp --> WorkerQueue
    FastAPIApp --> PostgresLMS
    FastAPIApp --> S3ObjectStore
    FastAPIApp --> RedisCache
    WorkerQueue --> PostgresLMS"""

        elif is_ecommerce:
            use_case = """graph LR
    subgraph Actors["E-Commerce Actors"]
        Customer["Customer / Buyer"]
        Merchant["Merchant / Seller"]
        Admin["Platform Admin"]
    end

    subgraph CoreSystem["E-Commerce Marketplace Boundary"]
        UC1(["Browse Products & Search"])
        UC2(["Add to Cart & Apply Coupon"])
        UC3(["Checkout & Pay via Stripe"])
        UC4(["Track Order & Shipment"])
        UC5(["Manage Catalog & Inventory"])
        UC6(["Process & Ship Orders"])
        UC7(["Manage Payouts & Commissions"])
    end

    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Merchant --> UC5
    Merchant --> UC6
    Admin --> UC7"""

            class_diag = """classDiagram
    class User {
        +UUID id
        +String email
        +String role
        +login() Boolean
    }

    class Customer {
        +UUID customer_id
        +String shipping_address
    }

    class Product {
        +UUID id
        +UUID vendor_id
        +String name
        +Decimal price
        +Integer stock_quantity
    }

    class CartItem {
        +UUID id
        +UUID customer_id
        +UUID product_id
        +Integer quantity
    }

    class Order {
        +UUID id
        +UUID customer_id
        +Decimal total_amount
        +String status
        +pay() Boolean
    }

    class OrderItem {
        +UUID id
        +UUID order_id
        +UUID product_id
        +Integer quantity
        +Decimal unit_price
    }

    User <|-- Customer
    Customer "1" --> "*" CartItem : has
    Customer "1" --> "*" Order : places
    Order "1" --> "*" OrderItem : contains
    Product "1" --> "*" OrderItem : ordered_as"""

            sequence_diag = """sequenceDiagram
    autonumber
    actor Customer
    participant Web as Storefront React
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant Stripe as Stripe Payment Gateway

    Customer->>Web: Click "Place Order & Pay"
    Web->>API: POST /api/checkout (CartItems, Address)
    API->>DB: Lock inventory & calculate order total
    API->>Stripe: Create PaymentIntent (Amount, Currency)
    Stripe-->>API: Client Secret returned
    API-->>Web: PaymentIntent Ready
    Web->>Stripe: Confirm payment with Card Token
    Stripe-->>Web: Payment Succeeded
    Web->>API: POST /api/orders/confirm (PaymentIntentId)
    API->>DB: UPDATE orders SET status='PAID', decrement inventory
    API-->>Web: Order Confirmed #ORD-9821
    Web-->>Customer: Display Order Confirmation Page"""

            activity_diag = """flowchart TD
    Start([Customer Adds Item to Cart]) --> ViewCart[Review Shopping Cart]
    ViewCart --> ProceedCheckout[Click Checkout]
    ProceedCheckout --> CheckAuth{Is Customer Logged In?}
    CheckAuth -- No --> PromptLogin[Login or Guest Checkout]
    PromptLogin --> InputShipping[Enter Shipping Address]
    CheckAuth -- Yes --> InputShipping
    InputShipping --> CheckInventory{Is Inventory In Stock?}
    CheckInventory -- No --> NotifyOOS[Notify Out of Stock & Adjust Cart]
    NotifyOOS --> ViewCart
    CheckInventory -- Yes --> LockInventory[Hold Stock for 10 Minutes]
    LockInventory --> ProcessPayment[Submit Payment to Stripe]
    ProcessPayment --> PaymentSuccess{Payment Successful?}
    PaymentSuccess -- No --> ShowPaymentError[Display Card Declined Error]
    ShowPaymentError --> ProcessPayment
    PaymentSuccess -- Yes --> CommitOrder[(Save Order & Deduct Inventory)]
    CommitOrder --> DispatchEmail[Dispatch Order Confirmation Email]
    DispatchEmail --> End([Order Placed Successfully])"""

            component_diag = """flowchart TB
    subgraph FrontendTier["Storefront"]
        StoreWeb["React Storefront & Mobile Web"]
    end
    subgraph GatewayTier["API Gateway"]
        Nginx["Nginx Reverse Proxy"]
        BackendAPI["FastAPI E-Commerce Engine"]
    end
    subgraph DBTier["Persistence"]
        PostgreSQL[("PostgreSQL 16")]
        RedisStore[("Redis Carts & Session Cache")]
    end
    subgraph ExternalServices["External Payment"]
        StripeAPI["Stripe Payment Gateway"]
    end

    StoreWeb --> Nginx
    Nginx --> BackendAPI
    BackendAPI --> PostgreSQL
    BackendAPI --> RedisStore
    BackendAPI --> StripeAPI"""

        else:
            # Universal Semantic Architecture for any custom application
            info = self._extract_domain_entities(title, description)
            p_actor = info["primary_actor"]
            a_actor = info["admin_actor"]
            e1, e2, e3, e4 = info["e1"], info["e2"], info["e3"], info["e4"]

            use_case = f"""graph LR
    subgraph Actors["{title} Actors"]
        Act1["{p_actor}"]
        Act2["Operations Staff"]
        Act3["{a_actor}"]
    end

    subgraph CoreSystem["{title} System Boundary"]
        UC1(["Register & Authenticate Account"])
        UC2(["Search & Inspect {e1} Catalog"])
        UC3(["Create & Process {e2}"])
        UC4(["Schedule & Manage {e3}"])
        UC5(["Audit {e4} & Operational Logs"])
        UC6(["Generate Analytical Dashboards"])
        UC7(["Configure Platform Rules & Security"])
    end

    Act1 --> UC1
    Act1 --> UC2
    Act1 --> UC3
    Act1 --> UC4
    Act2 --> UC3
    Act2 --> UC4
    Act2 --> UC5
    Act3 --> UC5
    Act3 --> UC6
    Act3 --> UC7"""

            class_diag = f"""classDiagram
    class User {{
        +UUID id
        +String email
        +String password_hash
        +String role
        +Boolean is_active
        +Timestamp created_at
        +authenticate() Boolean
    }}

    class {e1} {{
        +UUID id
        +UUID user_id
        +String title
        +String status
        +Timestamp created_at
        +updateStatus(newStatus) Boolean
        +getDetails() Map
    }}

    class {e2} {{
        +UUID id
        +UUID {e1.lower()}_id
        +UUID user_id
        +Decimal amount
        +String status
        +DateTime processed_at
        +execute() Boolean
        +cancel() Boolean
    }}

    class {e3} {{
        +UUID id
        +UUID {e1.lower()}_id
        +DateTime scheduled_time
        +String notes
        +reschedule(newTime) Boolean
    }}

    class {e4} {{
        +UUID id
        +UUID {e2.lower()}_id
        +String record_data
        +Timestamp logged_at
        +generateReport() String
    }}

    User "1" --> "*" {e1} : manages
    User "1" --> "*" {e2} : initiates
    {e1} "1" --> "*" {e2} : associates_with
    {e1} "1" --> "*" {e3} : schedules
    {e2} "1" --> "1" {e4} : logs"""

            sequence_diag = f"""sequenceDiagram
    autonumber
    actor Client as {p_actor}
    participant Web as React SPA
    participant API as FastAPI Backend
    participant DB as PostgreSQL Database
    participant Worker as Background Task Engine

    Client->>Web: Initiate new {e2} for {e1}
    Web->>API: POST /api/{e2.lower()}s (Payload, Bearer Token)
    API->>DB: Check {e1} state & verify permissions
    alt {e1} Available & Valid
        DB-->>API: State Confirmed
        API->>DB: INSERT INTO {e2.lower()}s (status='CONFIRMED')
        DB-->>API: {e2} Record Committed
        API-)Worker: Dispatch background event notification
        API-->>Web: HTTP 201 Created ({e2} Details)
        Web-->>Client: Display Success Confirmation & Receipt
    else Conflict / Invalid
        DB-->>API: State Conflict Detected
        API-->>Web: HTTP 409 Conflict ({e1} unavailable)
        Web-->>Client: Prompt to adjust parameters
    end"""

            activity_diag = f"""flowchart TD
    Start([Initiate {e2} Process]) --> CheckAuth{{"Is User Authenticated?"}}
    CheckAuth -- No --> PromptLogin[Redirect to Login / Registration]
    PromptLogin --> Validate{e1}[Validate {e1} Parameters]
    CheckAuth -- Yes --> Validate{e1}
    Validate{e1} --> CheckAvailability{{"Is {e1} Available?"}}
    CheckAvailability -- No --> ShowError[Display Conflict Error Message]
    ShowError --> EndNode1([Process Terminated])
    CheckAvailability -- Yes --> Process{e2}[Execute {e2} Business Logic]
    Process{e2} --> CommitDB[(Commit {e2} Transaction to PostgreSQL)]
    CommitDB --> RecordLog[Emit {e4} Audit Event]
    RecordLog --> SendAlert[Dispatch Push Notification & Email]
    SendAlert --> EndNode2([Completed Successfully])"""

            component_diag = f"""flowchart TB
    subgraph PresentationTier["Presentation Tier"]
        ClientApp["React SPA ({title} Web UI)"]
        MobileApp["Mobile Responsive View"]
    end

    subgraph APITier["Application & API Gateway"]
        Nginx["Nginx Reverse Proxy & Load Balancer"]
        FastAPICore["FastAPI REST Application Services"]
        AuthModule["JWT & Role-Based Access Control"]
        WorkerService["Background Event Worker"]
    end

    subgraph DataTier["Data & Persistence Tier"]
        PostgresDB[("PostgreSQL 16 ({e1}s, {e2}s, {e4}s)")]
        RedisCache[("Redis Session & Rate Limit Cache")]
    end

    ClientApp -->|HTTPS / JSON| Nginx
    MobileApp -->|HTTPS / JSON| Nginx
    Nginx --> FastAPICore
    FastAPICore --> AuthModule
    FastAPICore --> WorkerService
    FastAPICore --> PostgresDB
    FastAPICore --> RedisCache
    WorkerService --> PostgresDB"""

        return {
            "project_title": title,
            "use_case_diagram": use_case,
            "class_diagram": class_diag,
            "sequence_diagram": sequence_diag,
            "activity_diagram": activity_diag,
            "component_diagram": component_diag
        }

    def _generate_heuristic_db(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate normalized PostgreSQL schema and Mermaid ER diagram."""
        title_lower = title.lower()
        desc_lower = description.lower()

        is_hospital = "hosp" in title_lower or "clinic" in title_lower or "health" in desc_lower or "patient" in desc_lower
        is_lms = "lms" in title_lower or "learn" in title_lower or "course" in title_lower or "student" in desc_lower or "school" in title_lower or "edtech" in title_lower or "teach" in desc_lower
        is_ecommerce = "shop" in title_lower or "store" in title_lower or "e-commerce" in title_lower or "marketplace" in title_lower or "cart" in desc_lower or "retail" in desc_lower

        if is_hospital:
            er_diagram = """erDiagram
    USERS ||--o| PATIENTS : "identifies as"
    USERS ||--o| DOCTORS : "identifies as"
    PATIENTS ||--o{ APPOINTMENTS : "schedules"
    DOCTORS ||--o{ APPOINTMENTS : "attends"
    PATIENTS ||--o{ MEDICAL_RECORDS : "possesses"
    DOCTORS ||--o{ MEDICAL_RECORDS : "authors"
    MEDICAL_RECORDS ||--o{ PRESCRIPTIONS : "generates"
    PATIENTS ||--o{ INVOICES : "billed to"
    INVOICES ||--|{ INVOICE_ITEMS : "contains"

    USERS {
        uuid id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        timestamp created_at
    }

    PATIENTS {
        uuid id PK
        uuid user_id FK
        string mrn_number UK
        string full_name
        date date_of_birth
        string gender
        string blood_group
        string contact_phone
    }

    DOCTORS {
        uuid id PK
        uuid user_id FK
        string full_name
        string specialization
        string license_number UK
        decimal consultation_fee
    }

    APPOINTMENTS {
        uuid id PK
        uuid patient_id FK
        uuid doctor_id FK
        timestamp scheduled_start
        timestamp scheduled_end
        string status
        text symptoms
        timestamp created_at
    }

    MEDICAL_RECORDS {
        uuid id PK
        uuid patient_id FK
        uuid doctor_id FK
        uuid appointment_id FK
        text diagnosis
        text clinical_notes
        timestamp recorded_at
    }

    PRESCRIPTIONS {
        uuid id PK
        uuid record_id FK
        string medication_name
        string dosage
        string frequency
        integer duration_days
        string fulfillment_status
    }

    INVOICES {
        uuid id PK
        uuid patient_id FK
        decimal subtotal
        decimal tax
        decimal total_amount
        string payment_status
        timestamp issued_at
    }

    INVOICE_ITEMS {
        uuid id PK
        uuid invoice_id FK
        string item_description
        integer quantity
        decimal unit_price
        decimal total_price
    }"""

            sql_schema = """-- =======================================================
-- AI Software Architect: Normalized PostgreSQL Schema
-- System: Hospital Management System
-- Dialect: PostgreSQL 15+
-- =======================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'DOCTOR', 'PATIENT', 'PHARMACIST', 'BILLING')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    mrn_number VARCHAR(64) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10),
    contact_phone VARCHAR(50) NOT NULL,
    emergency_contact VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_mrn ON patients(mrn_number);

CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    specialization VARCHAR(150) NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    consultation_fee NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_doctors_specialization ON doctors(specialization);

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE RESTRICT,
    scheduled_start TIMESTAMP WITH TIME ZONE NOT NULL,
    scheduled_end TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'SCHEDULED' 
        CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    symptoms TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_appointment_times CHECK (scheduled_end > scheduled_start)
);

CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_schedule ON appointments(scheduled_start, status);

CREATE TABLE medical_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE RESTRICT,
    appointment_id UUID REFERENCES appointments(id) ON DELETE SET NULL,
    diagnosis TEXT NOT NULL,
    clinical_notes TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_records_patient ON medical_records(patient_id);

CREATE TABLE prescriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    record_id UUID NOT NULL REFERENCES medical_records(id) ON DELETE CASCADE,
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration_days INTEGER NOT NULL CHECK (duration_days > 0),
    fulfillment_status VARCHAR(30) DEFAULT 'PENDING' 
        CHECK (fulfillment_status IN ('PENDING', 'DISPENSED', 'CANCELLED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prescriptions_record ON prescriptions(record_id);

CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE RESTRICT,
    subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    tax NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    payment_status VARCHAR(30) DEFAULT 'UNPAID'
        CHECK (payment_status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID', 'REFUNDED')),
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoices_patient ON invoices(patient_id);
CREATE INDEX idx_invoices_status ON invoices(payment_status);

CREATE TABLE invoice_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    item_description VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_price NUMERIC(12, 2) NOT NULL CHECK (total_price >= 0)
);

CREATE INDEX idx_invoice_items_invoice ON invoice_items(invoice_id);
"""

            tables = [
                {
                    "name": "users",
                    "description": "System accounts for all system actors (Admins, Doctors, Patients, Pharmacists)",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Primary unique key"},
                        {"name": "email", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Unique user email"},
                        {"name": "password_hash", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Argon2/Bcrypt hash"},
                        {"name": "role", "data_type": "VARCHAR(50)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "RBAC user role"},
                        {"name": "is_active", "data_type": "BOOLEAN", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Account status flag"}
                    ]
                },
                {
                    "name": "patients",
                    "description": "Patient demographic records and emergency contact details",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Patient identifier"},
                        {"name": "user_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "users(id)", "is_nullable": False, "description": "Linked user account"},
                        {"name": "mrn_number", "data_type": "VARCHAR(64)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Medical Record Number"},
                        {"name": "full_name", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Legal patient name"}
                    ]
                },
                {
                    "name": "appointments",
                    "description": "Scheduled outpatient appointments between doctors and patients",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Appointment record key"},
                        {"name": "patient_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "patients(id)", "is_nullable": False, "description": "Assigned patient"},
                        {"name": "doctor_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "doctors(id)", "is_nullable": False, "description": "Assigned doctor"},
                        {"name": "scheduled_start", "data_type": "TIMESTAMPTZ", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Slot start timestamp"},
                        {"name": "status", "data_type": "VARCHAR(30)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Appointment status"}
                    ]
                }
            ]

            relationships = [
                {"from_table": "users", "to_table": "patients", "relationship_type": "one-to-one", "description": "User account identifies patient"},
                {"from_table": "users", "to_table": "doctors", "relationship_type": "one-to-one", "description": "User account identifies doctor"},
                {"from_table": "patients", "to_table": "appointments", "relationship_type": "one-to-many", "description": "Patient books many appointments"},
                {"from_table": "doctors", "to_table": "appointments", "relationship_type": "one-to-many", "description": "Doctor conducts many appointments"},
                {"from_table": "medical_records", "to_table": "prescriptions", "relationship_type": "one-to-many", "description": "Record contains prescriptions"},
                {"from_table": "invoices", "to_table": "invoice_items", "relationship_type": "one-to-many", "description": "Invoice itemizes line charges"}
            ]

        elif is_lms:
            er_diagram = """erDiagram
    USERS ||--o| STUDENTS : "identifies as"
    USERS ||--o| INSTRUCTORS : "identifies as"
    INSTRUCTORS ||--o{ COURSES : "authors"
    COURSES ||--|{ LESSONS : "contains"
    STUDENTS ||--o{ ENROLLMENTS : "enrolls"
    COURSES ||--o{ ENROLLMENTS : "receives"
    COURSES ||--o{ ASSIGNMENTS : "assigns"
    STUDENTS ||--o{ SUBMISSIONS : "submits"
    ASSIGNMENTS ||--o{ SUBMISSIONS : "evaluates"

    USERS {
        uuid id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        timestamp created_at
    }

    STUDENTS {
        uuid id PK
        uuid user_id FK
        string student_number UK
        string major
        timestamp enrolled_since
    }

    INSTRUCTORS {
        uuid id PK
        uuid user_id FK
        string full_name
        string department
        string bio
    }

    COURSES {
        uuid id PK
        uuid instructor_id FK
        string title
        text description
        decimal price
        boolean is_published
        timestamp created_at
    }

    LESSONS {
        uuid id PK
        uuid course_id FK
        string title
        string video_url
        integer order_index
        integer duration_minutes
    }

    ENROLLMENTS {
        uuid id PK
        uuid student_id FK
        uuid course_id FK
        decimal progress_percentage
        boolean is_completed
        timestamp enrolled_at
    }

    ASSIGNMENTS {
        uuid id PK
        uuid course_id FK
        string title
        text instructions
        integer max_score
        timestamp due_date
    }

    SUBMISSIONS {
        uuid id PK
        uuid assignment_id FK
        uuid student_id FK
        string file_url
        integer score
        text feedback
        timestamp submitted_at
    }"""

            sql_schema = """-- =======================================================
-- AI Software Architect: Normalized PostgreSQL Schema
-- System: Learning Management System (LMS)
-- Dialect: PostgreSQL 15+
-- =======================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'INSTRUCTOR', 'STUDENT')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    student_number VARCHAR(64) UNIQUE NOT NULL,
    major VARCHAR(150),
    enrolled_since TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE instructors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    department VARCHAR(150) NOT NULL,
    bio TEXT
);

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instructor_id UUID NOT NULL REFERENCES instructors(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_instructor ON courses(instructor_id);
CREATE INDEX idx_courses_published ON courses(is_published);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    video_url TEXT,
    order_index INTEGER NOT NULL DEFAULT 1,
    duration_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lessons_course ON lessons(course_id, order_index);

CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    progress_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id)
);

CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);

CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    instructions TEXT,
    max_score INTEGER NOT NULL DEFAULT 100,
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assignment_id UUID NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    file_url TEXT NOT NULL,
    score INTEGER CHECK (score >= 0),
    feedback TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(assignment_id, student_id)
);

CREATE INDEX idx_submissions_assignment ON submissions(assignment_id);
CREATE INDEX idx_submissions_student ON submissions(student_id);
"""

            tables = [
                {
                    "name": "users",
                    "description": "System authentication and RBAC user identities",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Primary key"},
                        {"name": "email", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Unique email"},
                        {"name": "role", "data_type": "VARCHAR(50)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "STUDENT | INSTRUCTOR | ADMIN"}
                    ]
                },
                {
                    "name": "courses",
                    "description": "Curriculum units authored by instructors",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Course identifier"},
                        {"name": "instructor_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "instructors(id)", "is_nullable": False, "description": "Course author"},
                        {"name": "title", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Course title"}
                    ]
                },
                {
                    "name": "enrollments",
                    "description": "Records student participation and progress in courses",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Enrollment record"},
                        {"name": "student_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "students(id)", "is_nullable": False, "description": "Enrolled student"},
                        {"name": "course_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "courses(id)", "is_nullable": False, "description": "Selected course"}
                    ]
                }
            ]

            relationships = [
                {"from_table": "users", "to_table": "students", "relationship_type": "one-to-one", "description": "User identity represents student"},
                {"from_table": "users", "to_table": "instructors", "relationship_type": "one-to-one", "description": "User identity represents instructor"},
                {"from_table": "instructors", "to_table": "courses", "relationship_type": "one-to-many", "description": "Instructor authors courses"},
                {"from_table": "courses", "to_table": "lessons", "relationship_type": "one-to-many", "description": "Course organizes lessons"},
                {"from_table": "students", "to_table": "enrollments", "relationship_type": "one-to-many", "description": "Student holds enrollments"},
                {"from_table": "assignments", "to_table": "submissions", "relationship_type": "one-to-many", "description": "Assignment collects submissions"}
            ]

        elif is_ecommerce:
            er_diagram = """erDiagram
    USERS ||--o| CUSTOMERS : "identifies as"
    USERS ||--o| MERCHANTS : "identifies as"
    MERCHANTS ||--o{ PRODUCTS : "sells"
    CUSTOMERS ||--o{ ORDERS : "places"
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "part of"
    ORDERS ||--o| PAYMENTS : "settled via"

    USERS {
        uuid id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        timestamp created_at
    }

    CUSTOMERS {
        uuid id PK
        uuid user_id FK
        string full_name
        text shipping_address
    }

    MERCHANTS {
        uuid id PK
        uuid user_id FK
        string store_name UK
        decimal commission_rate
    }

    PRODUCTS {
        uuid id PK
        uuid merchant_id FK
        string title
        decimal price
        integer stock_quantity
    }

    ORDERS {
        uuid id PK
        uuid customer_id FK
        decimal total_amount
        string order_status
        timestamp placed_at
    }

    ORDER_ITEMS {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        integer quantity
        decimal unit_price
    }

    PAYMENTS {
        uuid id PK
        uuid order_id FK
        decimal amount
        string payment_gateway_id
        string status
    }"""

            sql_schema = """-- =======================================================
-- AI Software Architect: Normalized PostgreSQL Schema
-- System: E-Commerce Marketplace
-- Dialect: PostgreSQL 15+
-- =======================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'MERCHANT', 'CUSTOMER')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    shipping_address TEXT NOT NULL
);

CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    store_name VARCHAR(255) UNIQUE NOT NULL,
    commission_rate NUMERIC(5, 2) NOT NULL DEFAULT 5.00
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_merchant ON products(merchant_id);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    order_status VARCHAR(50) NOT NULL DEFAULT 'PENDING' 
        CHECK (order_status IN ('PENDING', 'PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED')),
    placed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_customer ON orders(customer_id);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0)
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID UNIQUE NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL,
    payment_gateway_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'COMPLETED'
);
"""

            tables = [
                {
                    "name": "products",
                    "description": "Merchant catalog listings with pricing and stock",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Product ID"},
                        {"name": "merchant_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "merchants(id)", "is_nullable": False, "description": "Seller"},
                        {"name": "title", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Item name"},
                        {"name": "price", "data_type": "NUMERIC(10,2)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Retail price"}
                    ]
                },
                {
                    "name": "orders",
                    "description": "Customer purchase orders and fulfillment state",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Order number"},
                        {"name": "customer_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "customers(id)", "is_nullable": False, "description": "Buyer"},
                        {"name": "order_status", "data_type": "VARCHAR(50)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Order lifecycle"}
                    ]
                }
            ]

            relationships = [
                {"from_table": "merchants", "to_table": "products", "relationship_type": "one-to-many", "description": "Merchant stocks products"},
                {"from_table": "customers", "to_table": "orders", "relationship_type": "one-to-many", "description": "Customer places orders"},
                {"from_table": "orders", "to_table": "order_items", "relationship_type": "one-to-many", "description": "Order aggregates line items"}
            ]

        else:
            # Universal Semantic Database Schema
            info = self._extract_domain_entities(title, description)
            p_actor = info["primary_actor"]
            e1, e2, e3, e4 = info["e1"], info["e2"], info["e3"], info["e4"]

            er_diagram = f"""erDiagram
    USERS ||--o{{ {e1.upper()}S : "manages"
    USERS ||--o{{ {e2.upper()}S : "initiates"
    {e1.upper()}S ||--o{{ {e2.upper()}S : "includes"
    {e1.upper()}S ||--o{{ {e3.upper()}S : "schedules"
    {e2.upper()}S ||--o| {e4.upper()}S : "logs"

    USERS {{
        uuid id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        timestamp created_at
    }}

    {e1.upper()}S {{
        uuid id PK
        uuid user_id FK
        string title
        string status
        timestamp created_at
    }}

    {e2.upper()}S {{
        uuid id PK
        uuid {e1.lower()}_id FK
        uuid user_id FK
        decimal amount
        string status
        timestamp processed_at
    }}

    {e3.upper()}S {{
        uuid id PK
        uuid {e1.lower()}_id FK
        timestamp scheduled_time
        string notes
    }}

    {e4.upper()}S {{
        uuid id PK
        uuid {e2.lower()}_id FK
        string record_data
        timestamp logged_at
    }}"""

            sql_schema = f"""-- =======================================================
-- AI Software Architect: Normalized PostgreSQL Schema
-- System: {title}
-- Dialect: PostgreSQL 15+
-- =======================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE {e1.lower()}s (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_{e1.lower()}s_user ON {e1.lower()}s(user_id);
CREATE INDEX idx_{e1.lower()}s_status ON {e1.lower()}s(status);

CREATE TABLE {e2.lower()}s (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    {e1.lower()}_id UUID NOT NULL REFERENCES {e1.lower()}s(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_{e2.lower()}s_{e1.lower()} ON {e2.lower()}s({e1.lower()}_id);
CREATE INDEX idx_{e2.lower()}s_user ON {e2.lower()}s(user_id);

CREATE TABLE {e3.lower()}s (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    {e1.lower()}_id UUID NOT NULL REFERENCES {e1.lower()}s(id) ON DELETE CASCADE,
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_{e3.lower()}s_{e1.lower()} ON {e3.lower()}s({e1.lower()}_id);

CREATE TABLE {e4.lower()}s (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    {e2.lower()}_id UUID NOT NULL REFERENCES {e2.lower()}s(id) ON DELETE CASCADE,
    record_data TEXT,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_{e4.lower()}s_{e2.lower()} ON {e4.lower()}s({e2.lower()}_id);
"""
            tables = [
                {
                    "name": "users",
                    "description": "User accounts and authentication credentials",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Primary key"},
                        {"name": "email", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Unique email address"}
                    ]
                },
                {
                    "name": f"{e1.lower()}s",
                    "description": f"Primary {e1} catalog and resource records",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Primary key"},
                        {"name": "user_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": "users(id)", "is_nullable": False, "description": "Owner identifier"},
                        {"name": "title", "data_type": "VARCHAR(255)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": f"{e1} title"},
                        {"name": "status", "data_type": "VARCHAR(50)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Current lifecycle status"}
                    ]
                },
                {
                    "name": f"{e2.lower()}s",
                    "description": f"Transactional {e2} events linked to {e1}",
                    "columns": [
                        {"name": "id", "data_type": "UUID", "is_primary_key": True, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Primary key"},
                        {"name": f"{e1.lower()}_id", "data_type": "UUID", "is_primary_key": False, "is_foreign_key": True, "references": f"{e1.lower()}s(id)", "is_nullable": False, "description": f"Linked {e1}"},
                        {"name": "amount", "data_type": "NUMERIC(12,2)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Monetary or unit value"},
                        {"name": "status", "data_type": "VARCHAR(50)", "is_primary_key": False, "is_foreign_key": False, "references": None, "is_nullable": False, "description": "Processing status"}
                    ]
                }
            ]

            relationships = [
                {"from_table": "users", "to_table": f"{e1.lower()}s", "relationship_type": "one-to-many", "description": f"User manages {e1}s"},
                {"from_table": f"{e1.lower()}s", "to_table": f"{e2.lower()}s", "relationship_type": "one-to-many", "description": f"{e1} participates in {e2}s"},
                {"from_table": f"{e1.lower()}s", "to_table": f"{e3.lower()}s", "relationship_type": "one-to-many", "description": f"{e1} scheduled via {e3}s"}
            ]

        return {
            "project_title": title,
            "er_diagram": er_diagram,
            "sql_schema": sql_schema,
            "tables": tables,
            "relationships": relationships
        }

    async def analyze_requirements(self, title: str, description: str, domain: str) -> Dict[str, Any]:
        """Analyze project requirements with LLM or fallback engine."""
        prompt = f"Project Title: {title}\nDomain: {domain}\nDescription: {description}"
        result = await self._call_llm(REQUIREMENT_ANALYSIS_SYSTEM_PROMPT, prompt)
        if result and "functional_requirements" in result:
            return result
        return self._generate_heuristic_requirements(title, description, domain)

    async def generate_srs(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate IEEE-style SRS specification."""
        prompt = f"Project Title: {title}\nDescription: {description}\nRequirements Analysis Context:\n{json.dumps(analysis)}"
        result = await self._call_llm(SRS_SYSTEM_PROMPT, prompt)
        if result and "markdown_content" in result:
            return result
        return self._generate_heuristic_srs(title, description, analysis)

    async def generate_uml(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 5 Mermaid UML diagrams."""
        prompt = f"Project Title: {title}\nDescription: {description}\nRequirements Analysis Context:\n{json.dumps(analysis)}"
        result = await self._call_llm(UML_SYSTEM_PROMPT, prompt)
        if result and "use_case_diagram" in result and "class_diagram" in result:
            return result
        return self._generate_heuristic_uml(title, description, analysis)

    async def generate_database_design(self, title: str, description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate normalized PostgreSQL schema and Mermaid ER diagram."""
        prompt = f"Project Title: {title}\nDescription: {description}\nRequirements Analysis Context:\n{json.dumps(analysis)}"
        result = await self._call_llm(DB_DESIGN_SYSTEM_PROMPT, prompt)
        if result and "er_diagram" in result and "sql_schema" in result:
            return result
        return self._generate_heuristic_db(title, description, analysis)

ai_service = AIService()
