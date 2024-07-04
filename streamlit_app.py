# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie:cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be: ',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_List = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections = 4
    )
#ingredients_string = ''
if ingredients_List:
    ingredients_string = ''

    for fruit_Chosen in ingredients_List:
        ingredients_string += fruit_Chosen +  ' '
        
#st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered, name_on_orders!', icon="✅")
        
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
    
