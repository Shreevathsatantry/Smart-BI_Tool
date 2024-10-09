import streamlit as st
import pandas as pd
import plotly.express as px

# Set wide layout for the app
st.set_page_config(layout="wide")
def show_page():
    # Title of the app
    st.title("Interactive Dashboard")
    
    # Sidebar for CSV Input
    st.sidebar.header("Upload your CSV file")
    csv_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    # Caching the data loading to optimize performance
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file, encoding='ISO-8859-1')
    
    # Check if the file is uploaded and load the dataset
    if csv_file:
        try:
            # Load dataset once using cache
            df = load_data(csv_file)
            st.sidebar.subheader("Preview Data")
    
            # Show a checkbox for data preview (sampled to optimize performance)
            if st.sidebar.checkbox("Preview the dataset"):
                st.write(df.head(100))  # Show only first 100 rows for preview
    
            # Show a checkbox for summary statistics (optional)
            if st.sidebar.checkbox("Show Summary Statistics"):
                st.write(df.describe())
    
            # Filter Option
            st.sidebar.subheader("Filter Data")
            filter_column = st.sidebar.selectbox("Select a column to filter by", ['None'] + df.columns.tolist())
    
            # Apply filter based on user selection
            if filter_column != 'None':
                unique_values = ['None'] + df[filter_column].unique().tolist()
                selected_value = st.sidebar.selectbox(f"Select a value from {filter_column}", unique_values)
    
                # If a specific value is selected, filter the dataset
                if selected_value != 'None':
                    df = df[df[filter_column] == selected_value]
    
            # Graph Selection
            st.sidebar.subheader("Select Graphs")
            graph_options = []
            if st.sidebar.checkbox("Bar Plot"):
                graph_options.append("Bar Plot")
            if st.sidebar.checkbox("Pie Chart"):
                graph_options.append("Pie Chart")
            if st.sidebar.checkbox("Time Series Plot"):
                graph_options.append("Time Series Plot")
            if st.sidebar.checkbox("Scatter Plot"):
                graph_options.append("Scatter Plot")
            if st.sidebar.checkbox("Histogram"):
                graph_options.append("Histogram")
            if st.sidebar.checkbox("Box Plot"):
                graph_options.append("Box Plot")
            if st.sidebar.checkbox("Bubble Chart"):
                graph_options.append("Bubble Chart")
            if st.sidebar.checkbox("Treemap"):
                graph_options.append("Treemap")
            if st.sidebar.checkbox("Correlation Heatmap"):
                graph_options.append("Correlation Heatmap")
    
            # Color Pickers
            st.sidebar.subheader("Graph Colors")
            bar_color = st.sidebar.color_picker('Select Bar Plot Color', '#00f900')
            pie_color = st.sidebar.color_picker('Select Pie Chart Color', '#ff5733')
            line_color = st.sidebar.color_picker('Select Line Plot Color', '#007bff')
            scatter_color = st.sidebar.color_picker('Select Scatter Plot Color', '#17becf')
            histogram_color = st.sidebar.color_picker('Select Histogram Color', '#ffbf00')
            box_color = st.sidebar.color_picker('Select Box Plot Color', '#ff6347')
            bubble_color = st.sidebar.color_picker('Select Bubble Chart Color', '#ff8c00')
            treemap_color = st.sidebar.color_picker('Select Treemap Color', '#ff6600')
    
            # Arrange graphs alternately
            col1, col2 = st.columns(2)
            graph_counter = 0  # Initialize the counter
    
            def assign_column(graph_component):
                """Assigns the current graph to col1 or col2 based on the counter."""
                nonlocal graph_counter  # Declare graph_counter as nonlocal
                if graph_counter % 2 == 0:
                    with col1:
                        graph_component()
                else:
                    with col2:
                        graph_component()
                graph_counter += 1  # Increment the counter
    
            # Generating graphs
            if "Bar Plot" in graph_options:
                def bar_plot():
                    st.subheader("Interactive Bar Plot")
                    x_axis = st.selectbox('Select X-axis:', df.columns)
                    y_axis = st.selectbox('Select Y-axis:', df.select_dtypes(['number']).columns)
                    fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Plot", color_discrete_sequence=[bar_color])
                    st.plotly_chart(fig)
    
                assign_column(bar_plot)
    
            if "Pie Chart" in graph_options:
                def pie_chart():
                    st.subheader("Interactive Pie Chart")
                    category_column = st.selectbox('Select Categorical Column for Pie Chart', df.select_dtypes(['object']).columns)
                    fig = px.pie(df, names=category_column, title="Pie Chart", color_discrete_sequence=[pie_color])
                    st.plotly_chart(fig)
    
                assign_column(pie_chart)
    
            if "Time Series Plot" in graph_options:
                def time_series_plot():
                    st.subheader("Interactive Time Series Plot")
                    date_column = st.selectbox("Select Date Column", df.select_dtypes(['object', 'datetime']).columns)
                    value_column = st.selectbox("Select Value Column", df.select_dtypes(['number']).columns)
                    fig = px.line(df, x=date_column, y=value_column, title="Time Series Plot",
                                  line_shape='linear', color_discrete_sequence=[line_color])
                    st.plotly_chart(fig)
    
                assign_column(time_series_plot)
    
            if "Scatter Plot" in graph_options:
                def scatter_plot():
                    st.subheader("Interactive Scatter Plot")
                    x_axis = st.selectbox('Select X-axis for Scatter Plot:', df.select_dtypes(['number']).columns)
                    y_axis = st.selectbox('Select Y-axis for Scatter Plot:', df.select_dtypes(['number']).columns)
                    fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot", color_discrete_sequence=[scatter_color])
                    st.plotly_chart(fig)
    
                assign_column(scatter_plot)
    
            if "Histogram" in graph_options:
                def histogram():
                    st.subheader("Interactive Histogram")
                    hist_column = st.selectbox("Select Column for Histogram", df.select_dtypes(['number']).columns)
                    fig = px.histogram(df, x=hist_column, title="Histogram", color_discrete_sequence=[histogram_color])
                    st.plotly_chart(fig)
    
                assign_column(histogram)
    
            if "Box Plot" in graph_options:
                def box_plot():
                    st.subheader("Interactive Box Plot")
                    y_axis = st.selectbox("Select Y-axis for Box Plot", df.select_dtypes(['number']).columns)
                    fig = px.box(df, y=y_axis, title="Box Plot", color_discrete_sequence=[box_color])
                    st.plotly_chart(fig)
    
                assign_column(box_plot)
    
            if "Bubble Chart" in graph_options:
                def bubble_chart():
                    st.subheader("Interactive Bubble Chart")
                    x_axis = st.selectbox("Select X-axis for Bubble Chart", df.select_dtypes(['number']).columns)
                    y_axis = st.selectbox("Select Y-axis for Bubble Chart", df.select_dtypes(['number']).columns)
                    size_column = st.selectbox("Select Size Column for Bubble Chart", df.select_dtypes(['number']).columns)
                    fig = px.scatter(df, x=x_axis, y=y_axis, size=size_column, title="Bubble Chart", color_discrete_sequence=[bubble_color])
                    st.plotly_chart(fig)
    
                assign_column(bubble_chart)
    
            if "Treemap" in graph_options:
                def treemap():
                    st.subheader("Interactive Treemap")
                    category_column = st.selectbox("Select Category for Treemap", df.select_dtypes(['object']).columns)
                    value_column = st.selectbox("Select Value for Treemap", df.select_dtypes(['number']).columns)
                    fig = px.treemap(df, path=[category_column], values=value_column, title="Treemap", color_discrete_sequence=[treemap_color])
                    st.plotly_chart(fig)
    
                assign_column(treemap)
    
            if "Correlation Heatmap" in graph_options:
                def heatmap():
                    st.subheader("Interactive Correlation Heatmap")
                    selected_columns = st.multiselect("Select Columns for Heatmap (at least 2)", df.select_dtypes(['number']).columns)
    
                    if len(selected_columns) >= 2:
                        corr = df[selected_columns].corr()
                        fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap",
                                        color_continuous_scale='Viridis')
                        st.plotly_chart(fig)
                    else:
                        st.warning("Please select at least 2 numerical columns to generate the heatmap.")
    
                assign_column(heatmap)
    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.write("Please upload a valid CSV file to start.")

