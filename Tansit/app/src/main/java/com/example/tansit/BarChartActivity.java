package com.example.tansit;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;

public class BarChartActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bar_chart);

        BarChart barChart = findViewById(R.id.barChart);

        ArrayList<BarEntry> visitors = new ArrayList<>();
        visitors.add(new BarEntry(01,20));
        visitors.add(new BarEntry(02,25));
        visitors.add(new BarEntry(03,13));
        visitors.add(new BarEntry(04,27));
        visitors.add(new BarEntry(05,10));
        visitors.add(new BarEntry(06,30));
        visitors.add(new BarEntry(07,35));

        BarDataSet barDataSet = new BarDataSet(visitors, "Days (01:Mon, 02:Tue, 03:Wed, 04:Thurs, 05:Fri, 06:Sat, 07:Sun)");
        barDataSet.setColors(ColorTemplate.MATERIAL_COLORS);
        barDataSet.setValueTextColor(Color.BLACK);
        barDataSet.setValueTextSize(16f);

        BarData barData = new BarData(barDataSet);

        barChart.setFitBars(true);
        barChart.setData(barData);
        barChart.getDescription().setText("Average bus availability per day");
        barChart.animateX(2000);
        barChart.animateY(2000);
    }
}