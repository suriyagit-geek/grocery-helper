import streamlit as st
import csv

#browser title
st.set_page_config(
    page_title="Grocery Helper 🛒",
    layout="wide"
)

# Compact spacing
st.markdown("""
<style>

div[data-testid="stCheckbox"] {
    margin-bottom: -8px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.2rem;
}

</style>
""", unsafe_allow_html=True)

#page title
st.title("🛒 Grocery Helper")
st.write("Check the items you need to buy")

# Category colors
category_colors = {
    "Carb": "#F4A261",
    "Protein": "#4FC3F7",
    "Fat": "#FFD54F",

    "Vegetables Essential": "#66BB6A",   # Dark Green
    "Vegetables": "#A5D6A7",             # Light Green

    "Fruits": "#EF9A9A",
    "Snack ": "#CE93D8",
    "Beverage": "#90CAF9",

    "Home Care": "#B0BEC5",
    "Personal care": "#FFCC80",

    "spices": "#FFAB91",
    "spice powder": "#FFCCBC"
}

# Read CSV
with open("masterlist.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Custom category order
categories = [
    "Carb",
    "Protein",
    "Fat",

    "Vegetables Essential",
    "Vegetables",
    "Fruits",

    "Beverage",
    "Snack ",

    "spices",
    "spice powder",

    "Home Care",
    "Personal care"
]

selected_items = []

# Display categories - 2 per row
for start in range(0, len(categories), 2):

    cols = st.columns(2)

    for col_num in range(2):

        if start + col_num < len(categories):

            category = categories[start + col_num]

            with cols[col_num]:

                color = category_colors.get(category, "#E0E0E0")

                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:10px;
                        border-radius:10px;
                        font-weight:bold;
                        color:black;
                        margin-bottom:10px;
                    ">
                        📦 {category}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                items = [
                    row["Item"]
                    for row in data
                    if row["Category"] == category
                ]

                for item in items:

                    if st.checkbox(
                        item,
                        key=f"{category}_{item}"
                    ):
                        selected_items.append(item)

st.divider()

# Summary
selected_count = len(selected_items)
st.metric("Selected Items", selected_count)

# Shopping List

shopping_text = ""

for category in categories:

    category_items = []

    items = [
        row["Item"]
        for row in data
        if row["Category"] == category
    ]

    for item in items:

        if st.session_state.get(
            f"{category}_{item}",
            False
        ):
            category_items.append(item)

    if category_items:

        shopping_text += f"🛒 {category}\n"

        for item in category_items:
            shopping_text += f"- {item}\n"

        shopping_text += "\n"

st.markdown("### 🛒 Shopping List")

st.text_area(
    "Copy and Share",
    value=shopping_text,
    height=300
)

