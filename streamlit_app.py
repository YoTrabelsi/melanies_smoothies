# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

title = st.text_input('Name on Smoothie :')
st.write('The name on your Smoothie will be : ', title)

session = st.connection("snowflake").session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FrUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
'Choose up to 5 ingredients:',my_dataframe)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+=fruit+' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+title+ """')"""

    st.write(my_insert_stmt)
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)

