from stock_crypto_correlation import *

################################################################################################################################################
######################    main file to call functions laid out in previous file  ###############################################################
######################                                                           ###############################################################
################################################################################################################################################
#INPUTS
#CRYPTO
# -- TICKER 
# -- EXCHANGE
#STOCKS
# -- SYMBOL
#DATE PARAMETERS
# -- start date
# -- end date
##################################################################
#option = 'btcusd'
st.set_page_config(layout="wide")
projectlist = ["Ethereum", "Bitcoin","Cardano","DogeCoin","PolkaDot","Avalanche","Solana","Litecoin","Zcash"]
stocklist = ["QQQ", "AAPL", "ARKK", "NVDA", "SPAK","FFTY"  ]
#rollvol = RollingVolCrypto(json_to_df(cryptowatchAPIcall(option), option) )       

projectdict = {
    "ethusd":"Ethereum",
    "btcusd":"Bitcoin",
    "adausd":"Cardano",
    "dogeusd":"DogeCoin",
    "dotusd":"PolkaDot",
    "avaxusd":"Avalanche",
    "solusd":"Solana",
   "ltcusd":"Litecoin",
    "zecusd":"Zcash"
}
# function to return key for any value
def get_key(val):
    for key, value in projectdict.items():
         if val == value:
             return key


################################################################

st.title("Correlation Comparison --- Crypto Market vs Stock Market")
st.text("Due to the limitations of the API being used, and this being a fun project that I am unwilling to spend $100/month to maintain, an error will appear after making 1 or 2 calls per minute. I apologize for the inconevenience.")
st.text("If enough people find this information valuable please reach out to me on twitter @brush_10 as I would love to expand the project. Ideally I would scan a large list of protocols and compare them with various equities to")
st.text("identify correlation between a wide range of sectors/assets. Both Historical and emerging. ")
#option = get_key(slct)
slct = "Ethereum"
option2 = "QQQ"
col1, col2, col3 = st.columns([1,2,1])

with col1:
    slct = st.selectbox(
    'Select Protocol', projectlist)
    option = get_key(slct)

    st.write('You selected:', option)
    st.write(messariCryptoAPI(slct))
    # st.plotly_chart(RollingVolCrypto(json_to_df(cryptowatchAPIcall(option), option) ) , use_container_width=True)



with col3:
    date1 = st.date_input('start date', datetime(2022,3,1))
    st.write(date1)
    date2 = st.date_input('end date', datetime(2022,4,9))
    st.write(date2)
    option2 = st.selectbox(
    'Select Stock', stocklist)

    st.write('You selected:', option2)
    st.write("")

    st.write("Pearson Coeffecient")
    st.write(PearsonCorrValue(json_to_df(cryptowatchAPIcall(get_key(slct), date1, date2), get_key(slct), date1, date2),json_to_df2(PolygonAPIcall(option2, date1, date2), option2, date1, date2)))

with col2:
    st.plotly_chart(combineLinechart(json_to_df(cryptowatchAPIcall(get_key(slct), date1, date2), get_key(slct), date1, date2),json_to_df2(PolygonAPIcall(option2, date1, date2),option2, date1, date2) , get_key(slct), option2), use_container_width=True)
    st.plotly_chart(logLinechart(json_to_df(cryptowatchAPIcall(get_key(slct), date1, date2), get_key(slct), date1, date2) ,json_to_df2(PolygonAPIcall(option2, date1, date2), option2, date1, date2), get_key(slct), option2), use_container_width=True)




#json_to_df(cryptowatchAPIcall(option), option)                                 #GET ANY CRYPTO CHART AND OUTPUT TO DF

#stockDF = json_to_df2(PolygonAPIcall())                                     #GET ANY STOCK CHART AND OUTPUT TO DF

#double_line_chart = combineLinechart(json_to_df(cryptowatchAPIcall(option)) ,stockDF)               #GET OVERLAY OF PRICE BETWEEN SELECTED INPUTS

# double_log_chart = logLinechart(json_to_df(cryptowatchAPIcall(option), option) ,stockDF, option)                  #GET OVERLAY OF LOG RETURN BETWEEN SELECTED INPUTS

# PearsonValue = PearsonCorrValue(json_to_df(cryptowatchAPIcall(option), option) ,stockDF)                           #GET DF OF PEARSON COEFFECIENT 
                                                            
# rollingCorr = ROLLINGcorrelation(json_to_df(cryptowatchAPIcall(option), option) , stockDF)                         #GET ROLLING CORRELATION (DEFAULT 20 days) OUTPUT LINE CHART 

                                 #GET WEEKLY ROLLING VOLATILITY OF CRYPTO ASSET 

#####################################################################




#st.plotly_chart(combineLinechart(json_to_df(cryptowatchAPIcall(option), option),stockDF, option), use_container_width=True)

#st.plotly_chart(double_log_chart, use_container_width=True)

#st.plotly_chart(rollingCorr, use_container_width=True)
