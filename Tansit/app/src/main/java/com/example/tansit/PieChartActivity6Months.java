package com.example.tansit;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;

public class PieChartActivity6Months extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pie_chart_activity6_months);

        PieChart pieChart = findViewById(R.id.pieChart6months);

        ArrayList<PieEntry> buses = new ArrayList<>();
        buses.add(new PieEntry(70, "B10"));
        buses.add(new PieEntry(25, "B11"));
        buses.add(new PieEntry(18, "B12"));
        buses.add(new PieEntry(20, "B13"));
        buses.add(new PieEntry(35, "B14"));


        PieDataSet pieDataSet = new PieDataSet(buses, "Buses");
        pieDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
        pieDataSet.setValueTextColor(Color.BLACK);
        pieDataSet.setValueTextSize(16f);

        PieData pieData1 = new PieData(pieDataSet);

        pieChart.setData(pieData1);
        pieChart.getDescription().setEnabled(false);
        pieChart.setCenterText("Time taken by each bus in past journey (6 Months)");
        pieChart.animate();
    }
}