from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import gridplot, grid
from bokeh.models import ColumnDataSource, HoverTool, TapTool, TextInput, Select
from bokeh.models.callbacks import CustomJS
import numpy as np
import pandas as pd
from bokeh.events import Tap

# xrk file exported as a csv from race studio for now
filename = 'C:/Users/hamza/Downloads/Can_FUBC15_North Parkade Roof_Generic testing_b_2505.csv'

# load in data
data = np.loadtxt(filename, skiprows=25, delimiter=',')
time = data[:, 0]
oil_pressure = data[:, 28]
fuel_pressure = data[:, 27]
coolant_temp = data[:, 31]
throttle_pos = data[:, 24]

distance, logger_temp, external_voltage = data[:,1], data[:,2], data[:,3]
rear_brake, front_brake, steering_pos, accel_x, accel_y, accel_z = data[:,11], data[:,9], data[:,14], data[:,16], data[:,17], data[:,18]
gyro_x, gyro_y, gyro_z = data[:,19], data[:,20], data[:,21]
h_rpm, h_throttle, h_manif_pr, h_decel_cut, h_fuel_pr, h_oil_pr, h_clutch, h_lambda_1 = data[:,23], data[:,24], data[:,25], data[:,26], data[:,27], data[:,28], data[:,29], data[:,30]
h_coolant_t, h_air_t, h_oil_t, h_gear, h_trigger_cnt, h_home_cnt, h_miss_cnt, h_trigger_last = data[:,31], data[:,32], data[:,33], data[:,34], data[:,35], data[:,36], data[:,37], data[:,38]
h_inj_duty, h_ign_angle_le, h_batt_volt = data[:,39], data[:,40], data[:,42]

# ColumnDataSource
source = ColumnDataSource(
    data={'time': time, 'oil_pressure': oil_pressure, 'fuel_pressure': fuel_pressure, 'coolant_temp': coolant_temp,
          'throttle_position': throttle_pos})

source1 = ColumnDataSource(
    data={'time': time, 'oil_pressure': oil_pressure})

source2 = ColumnDataSource(
    data={'time': time, 'fuel_pressure': fuel_pressure})

source3 = ColumnDataSource(
    data={'time': time, 'coolant_temp': coolant_temp})

source4 = ColumnDataSource(
    data={'time': time, 'throttle_position': throttle_pos})

# glyphs = ["oil_pressure", "fuel_pressure", "coolant_temp", "throttle_pos"]

glyphs = ['distance', 'logger_temp', 'external_voltage', 'rear_brake', 'front_brake', 'steering_pos', 'accel_x', 'accel_y', 'accel_z',
           'gyro_x', 'gyro_y', 'gyro_z', 'h_rpm', 'h_throttle', 'h_manif_pr', 'h_decel_cut', 'h_fuel_pr', 'h_oil_pr', 'h_clutch',
           'h_lambda_1', 'h_coolant_t', 'h_air_t', 'h_oil_t', 'h_gear', 'h_trigger_cnt', 'h_home_cnt', 'h_miss_cnt', 'h_trigger_last',
           'h_inj_duty', 'h_ign_angle_le', 'h_batt_volt']

# side sensor value displays
time_value = TextInput(title="Time", value='', disabled=True, width=50, height=50)
oil_value = TextInput(title="Oil Pressure", value='', disabled=True, width=50, height=50)
coolant_value = TextInput(title="Coolant Temperature", value='', disabled=True, width=50)
fuel_value = TextInput(title="Fuel Pressure", value='', disabled=True, width=50)
throttle_value = TextInput(title="Throttle Position", value='', disabled=True, width=50)
select1 = Select(title="Select plot:", value="", options=[""] + glyphs)
select2 = Select(title="Select plot:", value="", options=[""] + glyphs)
select3 = Select(title="Select plot:", value="", options=[""] + glyphs)
select4 = Select(title="Select plot:", value="", options=[""] + glyphs)

oil = figure(title="Oil Pressure", x_axis_label="Time", y_axis_label="Oil Pressure", plot_width=700,
             plot_height=340, tools = "pan,wheel_zoom,box_zoom,reset")
oil.line(x='time', y='oil_pressure', legend_label="Oil Pressure", line_width=3, source=source1)

fuel = figure(title="Fuel Pressure", x_axis_label="Time", y_axis_label="Fuel Pressure", plot_width=700, plot_height=340, tools = "pan,wheel_zoom,box_zoom,reset")
fuel.line(x='time', y='fuel_pressure', legend_label="Fuel Pressure", line_width=3, source=source2)

coolant = figure(title="Coolant Temp", x_axis_label="Time", y_axis_label="Coolant Temp", plot_width=700,
                 plot_height=340, tools = "pan,wheel_zoom,box_zoom,reset")
coolant.line(x='time', y='coolant_temp', legend_label="Coolant Temp", line_width=3, source=source3)

throttle = figure(title="Throttle Position", x_axis_label="Time", y_axis_label="Throttle Position", plot_width=700,
                  plot_height=340, tools = "pan,wheel_zoom,box_zoom,reset")
throttle.line(x='time', y='throttle_position', legend_label="Throttle Position", line_width=3, source=source4)

###############################

callback_hover = CustomJS(
    args=dict(oil_value=oil_value, coolant_value=coolant_value, fuel_value=fuel_value, throttle_value=throttle_value,
              time_value=time_value, source=source), code="""
    var inds = cb_obj.indices;
    oil_value.value = source.data['oil_pressure'][cb_data['index'].line_indices] + '';
    coolant_value.value = source.data['coolant_temp'][cb_data['index'].line_indices] + '';
    fuel_value.value = source.data['fuel_pressure'][cb_data['index'].line_indices] + '';
    throttle_value.value = source.data['throttle_position'][cb_data['index'].line_indices] + '';
    time_value.value = source.data['time'][cb_data['index'].line_indices] + '';
    console.log(oil_value.value);
    console.log(coolant_value.value);
    console.log(fuel_value.value);
    console.log(throttle_value.value);
    console.log(time_value.value);
    """)


def onTab_oil(attr, old, new):
    print("tap:", oil_value.value)


# line_plot.data_source.on_change('selected',onTab_oil)
tap_tool = TapTool()

hover_tool = HoverTool(callback=callback_hover, mode='vline', tooltips=[("oil pressure", "@oil_pressure"), ("time", "@time")])
oil.add_tools(tap_tool)
oil.add_tools(hover_tool)
oil.toolbar.logo = None

hover_tool = HoverTool(callback=callback_hover, mode='vline', tooltips=[("fuel", "@fuel_pressure"), ("time", "@time")])
fuel.add_tools(tap_tool)
fuel.add_tools(hover_tool)
fuel.toolbar.logo = None

hover_tool = HoverTool(callback=callback_hover, mode='vline', tooltips=[("coolant", "@coolant_temp"), ("time", "@time")])
coolant.add_tools(tap_tool)
coolant.add_tools(hover_tool)
coolant.toolbar.logo = None

hover_tool = HoverTool(callback=callback_hover, mode='vline', tooltips=[("throttle", "@throttle_position"), ("time", "@time")])
throttle.add_tools(tap_tool)
throttle.add_tools(hover_tool)
throttle.toolbar.logo = None

def callback_plot1(attrname, old, new):
    sensor = select1.value
    newSource = data={'time': time, 'oil_pressure': eval(sensor)}
    source1.data = newSource
    oil.title.text = str(sensor)
    oil.yaxis.axis_label = str(sensor)

select1.on_change('value', callback_plot1)

def callback_plot2(attrname, old, new):
    sensor = select2.value
    newSource = data={'time': time, 'fuel_pressure': eval(sensor)}
    source2.data = newSource
    fuel.title.text = str(sensor)
    fuel.yaxis.axis_label = str(sensor)

select2.on_change('value', callback_plot2)

def callback_plot3(attrname, old, new):
    sensor = select3.value
    newSource = data = {'time': time, 'coolant_temp': eval(sensor)}
    source3.data = newSource
    coolant.title.text = str(sensor)
    coolant.yaxis.axis_label = str(sensor)

select3.on_change('value', callback_plot3)

def callback_plot4(attrname, old, new):
    sensor = select4.value
    newSource = data = {'time': time, 'throttle_position': eval(sensor)}
    source4.data = newSource
    throttle.title.text = str(sensor)
    throttle.yaxis.axis_label = str(sensor)

select4.on_change('value', callback_plot4)

###############################

grid = grid(
    [[time_value, oil_value, coolant_value, fuel_value, throttle_value], [select1, select2], [oil, fuel], [select3, select4], [coolant, throttle]])
# grid.max_height = 800
# grid.max_width = 1500
# curdoc().theme = 'dark_minimal'
curdoc().add_root(grid)