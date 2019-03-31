import pandas as pd
def time_of_day(dt_obj):
    """ Mapping function to return a string representing time of day for
    the departure or arrival datetime objects. """
    if dt_obj.hour < 8 and dt_obj.hour > 2:
        return 'early am'
    elif dt_obj.hour < 12:
        return 'morning'
    elif dt_obj.hour < 16:
        return 'afternoon'
    elif dt_obj.hour < 22:
        return 'evening'
    return 'late evening'
def prepare_final(final_df):
    """ Some cleaning for easy sort and comparison. """
    final_df['price'] = final_df.price.astype(float)
    final_df['duration_hours'] = final_df.duration_hours.astype(float)
    final_df['departure_tod'] = final_df.departure.map(time_of_day)
    return final_df

def prepare_sp_data(results):
    """ Prepare skypicker results so they can be easily compared. """
    sp_df = pd.DataFrame(results)
    sp_df['search_engine'] = 'SkyPicker'
    sp_df['num_stops'] = sp_df['legs'].map(lambda x: len(x) - 1)
    return sp_df

def convert_to_date_string(datetime_object):
    obj_str = str(datetime_object)
    year = obj_str[0:4]
    month = obj_str[5:7]
    day =  obj_str[8:10]
    return day + '/' + month + '/' + year

def convert_to_time_string(datetime_object):
    obj_str = str(datetime_object)
    return obj_str[11:19]
