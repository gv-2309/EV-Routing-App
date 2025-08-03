import streamlit as st
import pandas as pd
import numpy as np
import os
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from math import hypot

# --- Page Config ---
st.set_page_config(page_title="EV Routing Optimizer", layout="wide")

# --- Sidebar ---
st.sidebar.title("EV Routing Optimizer App")
mode = st.sidebar.radio("Select Input Mode", ["Use Test Case", "Upload Your Own File"])
uploaded_file = None

# --- File selection ---
if mode == "Use Test Case":
    test_dir = "Test_Case_CSV_Files"
    test_files = sorted([f for f in os.listdir(test_dir) if f.endswith(".csv")])
    selected_file = st.sidebar.selectbox("Choose Test Case", ["-- Select a test case --"] + test_files)

    if selected_file != "-- Select a test case --":
        file_path = os.path.join(test_dir, selected_file)
        uploaded_file = open(file_path, "rb")
        st.sidebar.success(f"Loaded: {selected_file}")
    else:
        st.sidebar.info("Please select a test case file to proceed.")

elif mode == "Upload Your Own File":
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

# --- Title
st.title("EV Routing with Discharge Station Optimization")

# --- If file uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_cols = {"ID", "X", "Y", "Demand", "NodeType"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must include columns: {required_cols}")
        else:
            st.markdown("### Input Data Preview")
            st.dataframe(df)

            discharge_mode = st.selectbox("Enable Discharge Mode?", ["No", "Yes"]) == "Yes"

            with st.form("vrp_form"):
                vehicle_count = st.number_input("Number of Vehicles", 1, 10, 2)
                capacity = st.number_input("Vehicle Capacity", 1, 1000, 100)
                submitted = st.form_submit_button("Solve VRP")

            if submitted:
                depot = df[df["NodeType"].str.lower() == "depot"].iloc[0]
                customers = df[df["NodeType"].str.lower() != "depot"].reset_index(drop=True)

                all_points = [(depot["X"], depot["Y"])] + list(zip(customers["X"], customers["Y"]))

                # Distance matrix
                def compute_distance_matrix(points):
                    return [
                        [int(hypot(x1 - x2, y1 - y2)) for (x2, y2) in points]
                        for (x1, y1) in points
                    ]

                distance_matrix = compute_distance_matrix(all_points)

                def solve_vrp(vehicle_count, capacity, depot, customers, distance_matrix, discharge_mode=False):
                    all_points = [(depot["X"], depot["Y"])] + list(zip(customers["X"], customers["Y"]))
                    demands = [0] + list(customers["Demand"])
                    penalties = [0]
                    for _, row in customers.iterrows():
                        if discharge_mode and row["NodeType"].lower() == "dischargestation":
                            penalties.append(-10)
                        else:
                            penalties.append(0)

                    manager = pywrapcp.RoutingIndexManager(len(all_points), vehicle_count, 0)
                    routing = pywrapcp.RoutingModel(manager)

                    def distance_callback(from_idx, to_idx):
                        from_node = manager.IndexToNode(from_idx)
                        to_node = manager.IndexToNode(to_idx)
                        return distance_matrix[from_node][to_node]

                    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                    def demand_callback(from_idx):
                        from_node = manager.IndexToNode(from_idx)
                        return demands[from_node]

                    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
                    routing.AddDimensionWithVehicleCapacity(
                        demand_callback_index,
                        0,
                        [capacity] * vehicle_count,
                        True,
                        "Capacity"
                    )

                    if discharge_mode:
                        for node in range(1, len(all_points)):
                            penalty = penalties[node]
                            if penalty < 0:
                                routing.AddDisjunction([manager.NodeToIndex(node)], -penalty)

                    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                    search_parameters.first_solution_strategy = (
                        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
                    )

                    solution = routing.SolveWithParameters(search_parameters)

                    output = []
                    if solution:
                        for vehicle_id in range(vehicle_count):
                            index = routing.Start(vehicle_id)
                            route = []
                            while not routing.IsEnd(index):
                                route.append(manager.IndexToNode(index))
                                index = solution.Value(routing.NextVar(index))
                            route.append(0)
                            output.append((vehicle_id, route))
                    return output

                solution = solve_vrp(vehicle_count, capacity, depot, customers, distance_matrix, discharge_mode)

                st.markdown("### Route Plan")
                if solution:
                    for vehicle_id, route in solution:
                        labels = []
                        for idx in route:
                            if idx == 0:
                                labels.append("Depot")
                            else:
                                node_type = customers.iloc[idx - 1]["NodeType"]
                                labels.append(f"{node_type} ({idx})")
                        st.write(f"**Vehicle {vehicle_id + 1}:** {' → '.join(labels)}")
                else:
                    st.warning("No solution found!")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file or select a test case to continue.")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align:center;">
    <strong>Developed by Team-Mind_Mesh</strong><br>
    Developers: Amrutha D , Vishnu V<br>
    College: REVA University, Bangalore<br>
    Contact: vishnuv2309@gmail.com
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    footer {visibility: hidden;}
    .stApp {bottom: 0;}
</style>
""", unsafe_allow_html=True)
# --- End of the app ---
