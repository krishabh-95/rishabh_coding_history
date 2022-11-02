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

public class PieChartActivity3months extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pie_chart_activity3months);

        PieChart pieChart = findViewById(R.id.pieChart3months);

        ArrayList<PieEntry> buses = new ArrayList<>();
        buses.add(new PieEntry(30, "B10"));
        buses.add(new PieEntry(45, "B11"));
        buses.add(new PieEntry(38, "B12"));
        buses.add(new PieEntry(60, "B13"));
        buses.add(new PieEntry(15, "B14"));


        PieDataSet pieDataSet = new PieDataSet(buses, "Buses");
        pieDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
        pieDataSet.setValueTextColor(Color.BLACK);
        pieDataSet.setValueTextSize(16f);

        PieData pieData2 = new PieData(pieDataSet);

        pieChart.setData(pieData2);
        pieChart.getDescription().setEnabled(false);
        pieChart.setCenterText("Time taken by each bus in past journey (3 Months)");
        pieChart.animate();
    }
}