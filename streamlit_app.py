# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
import requests
from snowflake.snowpark.functions import col



# Write directly to the app
st.title("Customize your own :blue[cool]:cup_with_straw: smoothie ")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingridients_list = st.multiselect(
    "Choose upto 5 ingridients", my_dataframe, max_selections=5)

if ingridients_list:    

    ingredients_string = ''

    for fruit_chosen in ingridients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen+ 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


