"""
=================================================================
 SIMATS ENGINEERING
 CSA10 - Software Engineering | Assignment 5
 Student: Musahith | Reg No: 192524400
 Faculty Guide: Dr. Ro.Mu. Jauhar
=================================================================

This file demonstrates the concepts discussed in the written
answers with small, runnable examples:

  Q1 - Technical Debt        : a "quick and dirty" function vs.
                                its refactored, debt-free version
  Q2 - AI/ML & Edge Computing: a lightweight "on-device" ML-style
                                inference example (edge) and a
                                simple predictive model (AI/ML)
  Q3 - Sustainable DevOps    : a mock auto-scaling / resource
                                monitor for cloud microservices

Run:  python assignment5.py
=================================================================
"""

import random
import time


# =================================================================
# QUESTION 1 — TECHNICAL DEBT
# =================================================================

def calc_total_BAD(items):
    """
    'Quick and dirty' version (illustrates technical debt):
    - no input validation
    - duplicated logic
    - magic numbers
    - no documentation
    """
    t = 0
    for i in items:
        t = t + i * 1.18  # 1.18 = tax, hardcoded magic number
    if t > 1000:
        t = t - t * 0.1  # discount, hardcoded, duplicated logic pattern
    return t


TAX_RATE = 0.18
BULK_DISCOUNT_THRESHOLD = 1000
BULK_DISCOUNT_RATE = 0.10


def calculate_total(prices, tax_rate=TAX_RATE,
                     discount_threshold=BULK_DISCOUNT_THRESHOLD,
                     discount_rate=BULK_DISCOUNT_RATE):
    """
    Refactored version — pays off the technical debt above:
    - validates input
    - named constants instead of magic numbers
    - clear, documented, testable logic
    """
    if not prices or any(p < 0 for p in prices):
        raise ValueError("prices must be a non-empty list of non-negative numbers")

    subtotal_with_tax = sum(prices) * (1 + tax_rate)

    if subtotal_with_tax > discount_threshold:
        subtotal_with_tax *= (1 - discount_rate)

    return round(subtotal_with_tax, 2)


def demo_technical_debt():
    print("\n--- Q1: Technical Debt Demo ---")
    prices = [250, 300, 500]
    print("Legacy (debt-laden) result :", round(calc_total_BAD(prices), 2))
    print("Refactored (clean) result  :", calculate_total(prices))


# =================================================================
# QUESTION 2 — AI/ML AND EDGE COMPUTING
# =================================================================

class SimpleFailureRiskModel:
    """
    A tiny stand-in for an AI/ML model used in software engineering,
    e.g., predicting which module is 'risky' based on historical
    metrics (lines changed, past bugs, code age).
    In practice this would be a trained ML model (e.g., scikit-learn);
    here we use simple weighted scoring to illustrate the idea.
    """

    def __init__(self, weight_changes=0.5, weight_bugs=1.5, weight_age=0.2):
        self.weight_changes = weight_changes
        self.weight_bugs = weight_bugs
        self.weight_age = weight_age

    def predict_risk(self, lines_changed, past_bugs, age_in_months):
        score = (lines_changed * self.weight_changes
                 + past_bugs * self.weight_bugs
                 + age_in_months * self.weight_age)
        risk = "HIGH" if score > 50 else "MEDIUM" if score > 20 else "LOW"
        return round(score, 2), risk


def edge_object_alert(sensor_reading):
    """
    Simulates an EDGE COMPUTING device (e.g., a smart camera) that
    processes data locally and only sends an alert to the cloud
    when something relevant is detected — instead of streaming
    everything to the cloud continuously.
    """
    detected_objects = sensor_reading.get("objects", [])
    if "person" in detected_objects or "vehicle" in detected_objects:
        return f"[EDGE DEVICE] Relevant event detected {detected_objects} -> sending alert to cloud"
    return "[EDGE DEVICE] Nothing relevant -> no data sent (saves bandwidth & energy)"


def demo_ai_edge():
    print("\n--- Q2: AI/ML Demo (defect-risk prediction) ---")
    model = SimpleFailureRiskModel()
    score, risk = model.predict_risk(lines_changed=40, past_bugs=6, age_in_months=24)
    print(f"Module risk score = {score} -> Risk level: {risk}")

    print("\n--- Q2: Edge Computing Demo (on-device filtering) ---")
    frames = [
        {"objects": []},
        {"objects": ["cat"]},
        {"objects": ["person"]},
    ]
    for frame in frames:
        print(edge_object_alert(frame))


# =================================================================
# QUESTION 3 — SUSTAINABLE DEVOPS (CASE STUDY)
# =================================================================

class Microservice:
    def __init__(self, name, base_load):
        self.name = name
        self.base_load = base_load
        self.instances = 1

    def current_load(self):
        # Simulated fluctuating traffic
        return max(0, self.base_load + random.randint(-20, 20))


def autoscale(service, load, max_instances=5, target_load_per_instance=40):
    """
    Sustainable DevOps Practice #1: Right-sizing / auto-scaling.
    Scales instances up under load and back down when idle,
    instead of always running at a fixed, over-provisioned size.
    """
    needed = max(1, min(max_instances, -(-load // target_load_per_instance)))  # ceil division
    if needed != service.instances:
        action = "UP" if needed > service.instances else "DOWN"
        print(f"  [{service.name}] scaling {action}: {service.instances} -> {needed} instance(s)")
        service.instances = needed
    else:
        print(f"  [{service.name}] stable at {service.instances} instance(s)")


def consolidate_services(services, capacity_per_node=3):
    """
    Sustainable DevOps Practice #2: Consolidation / bin-packing.
    Groups running instances onto the minimum number of nodes
    instead of spreading them thinly, reducing idle server energy use.
    """
    total_instances = sum(s.instances for s in services)
    nodes_needed = -(-total_instances // capacity_per_node)  # ceil division
    print(f"  Total instances: {total_instances} -> consolidated onto {nodes_needed} node(s) "
          f"(capacity {capacity_per_node} instances/node)")
    return nodes_needed


def carbon_aware_schedule(job_name, regions_carbon_intensity):
    """
    Sustainable DevOps Practice #3: Carbon-aware / green CI-CD scheduling.
    Picks the cloud region with the lowest carbon intensity to run
    a non-urgent batch job (e.g., nightly build, report generation).
    """
    best_region = min(regions_carbon_intensity, key=regions_carbon_intensity.get)
    print(f"  Scheduling '{job_name}' in region '{best_region}' "
          f"(lowest carbon intensity: {regions_carbon_intensity[best_region]} gCO2/kWh)")
    return best_region


def demo_sustainable_devops():
    print("\n--- Q3: Sustainable DevOps Demo ---")
    services = [
        Microservice("auth-service", base_load=60),
        Microservice("payment-service", base_load=90),
        Microservice("catalog-service", base_load=30),
    ]

    print("Practice 1: Auto-scaling based on live load")
    for s in services:
        autoscale(s, s.current_load())

    print("\nPractice 2: Consolidating onto fewer nodes")
    consolidate_services(services)

    print("\nPractice 3: Carbon-aware job scheduling")
    carbon_aware_schedule(
        "nightly-report-job",
        {"us-east": 410, "eu-north": 45, "ap-south": 620},
    )


# =================================================================
# MAIN
# =================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" CSA10 - Software Engineering | Assignment 5 - Code Demo")
    print("=" * 60)
    demo_technical_debt()
    demo_ai_edge()
    demo_sustainable_devops()
    print("\nDone.")
