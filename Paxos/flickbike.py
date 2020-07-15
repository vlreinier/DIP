from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import list_holidays as hd
from sklearn.metrics import mean_squared_error

# holidays and vacations
holidays, vacations = hd.holidays(), hd.vacations()

# train dataset
train_df = pd.read_csv("train.csv", index_col=0)
train_df["date"] = pd.to_datetime(train_df["date"], format="%Y-%m-%d %H:%M:%S")
train_df.head()

# prepare train dataset
daily_rentals_df = train_df[["tripid"]].groupby([train_df["date"].dt.date]).count()
daily_rentals_df.index = pd.to_datetime(daily_rentals_df.index, format="%Y-%m-%d")
daily_rentals_df['weekday'] = daily_rentals_df.index.weekday
daily_rentals_df.rename(columns={'tripid':'rented'},inplace=True)
daily_rentals_df["vacation"]=0
daily_rentals_df["holiday"]=0
for i in vacations:
    daily_rentals_df["vacation"][daily_rentals_df.index.isin(vacations[i])]=i
for i in holidays:
    daily_rentals_df["holiday"][daily_rentals_df.index.isin(holidays[i])]=i

# model training
train_X = daily_rentals_df[['weekday', 'vacation', 'holiday']]
train_y = daily_rentals_df['rented']

rfc = RandomForestClassifier(n_estimators=150, criterion='entropy', random_state=0).fit(train_X, train_y)

# test and verify dataset
verify_df = pd.read_csv("test.csv", index_col=0)
verify_df["date"] = pd.to_datetime(verify_df["date"], format="%Y-%m-%d %H:%M:%S")
verify_df.head()

# prepare test dataset
test_df = pd.DataFrame(pd.to_datetime(verify_df["date"].dt.date.unique()), columns=['date'])
test_df['weekday'] = pd.to_datetime(test_df['date']).dt.dayofweek
test_df.set_index("date", inplace=True)
test_df["vacation"]=0
test_df["holiday"]=0
for i in vacations:
    test_df["vacation"][test_df.index.isin(vacations[i])]=i
for i in holidays:
    test_df["holiday"][test_df.index.isin(holidays[i])]=i


def predict_daily_rentals(day):
    return rfc.predict(test_df.iloc[[int(day) + 1]])[0]