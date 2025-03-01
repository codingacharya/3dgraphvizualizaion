import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Streamlit page title
st.title("3D Graph Visualization")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.write(df.head())

    # Select columns for x, y, z axes
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_columns) < 3:
        st.error("Dataset must contain at least three numerical columns.")
    else:
        x_axis = st.selectbox("Select X-axis", numeric_columns)
        y_axis = st.selectbox("Select Y-axis", numeric_columns)
        z_axis = st.selectbox("Select Z-axis", numeric_columns)

        # Graph type selection
        graph_type = st.selectbox(
            "Select 3D Graph Type",
            [
                "Scatter Plot", "Surface Plot", "Wireframe Plot", "Contour Plot",
                "Mesh Plot", "Bubble Chart", "3D Bar Chart", "3D Histogram", "Density Plot"
            ]
        )

        fig = go.Figure()

        # Generate selected 3D plot
        if graph_type == "Scatter Plot":
            fig.add_trace(go.Scatter3d(x=df[x_axis], y=df[y_axis], z=df[z_axis], 
                                       mode='markers', marker=dict(size=5, color=df[z_axis], colorscale='Viridis')))

        elif graph_type == "Surface Plot":
            fig.add_trace(go.Surface(z=df.pivot(index=y_axis, columns=x_axis, values=z_axis).values))

        elif graph_type == "Wireframe Plot":
            fig.add_trace(go.Surface(z=df.pivot(index=y_axis, columns=x_axis, values=z_axis).values, 
                                     colorscale="gray", showscale=False, opacity=0.5))

        elif graph_type == "Contour Plot":
            fig.add_trace(go.Contour(x=df[x_axis], y=df[y_axis], z=df[z_axis], colorscale='Viridis'))

        elif graph_type == "Mesh Plot":
            fig.add_trace(go.Mesh3d(x=df[x_axis], y=df[y_axis], z=df[z_axis], color='lightblue', opacity=0.50))

        elif graph_type == "Bubble Chart":
            fig.add_trace(go.Scatter3d(x=df[x_axis], y=df[y_axis], z=df[z_axis], 
                                       mode='markers', marker=dict(size=df[z_axis]/df[z_axis].max()*20, color=df[z_axis], colorscale='Viridis')))

        elif graph_type == "3D Bar Chart":
            fig.add_trace(go.Bar3d(x=df[x_axis], y=df[y_axis], z=df[z_axis], 
                                   marker=dict(color=df[z_axis], colorscale='Viridis')))

        elif graph_type == "3D Histogram":
            fig.add_trace(go.Histogram3d(x=df[x_axis], y=df[y_axis], z=df[z_axis], colorscale='Viridis'))

        elif graph_type == "Density Plot":
            fig.add_trace(go.Densitymapbox(lat=df[x_axis], lon=df[y_axis], z=df[z_axis], radius=10, colorscale='Viridis'))

        # Set layout
        fig.update_layout(
            scene=dict(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                zaxis_title=z_axis
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        st.plotly_chart(fig)
