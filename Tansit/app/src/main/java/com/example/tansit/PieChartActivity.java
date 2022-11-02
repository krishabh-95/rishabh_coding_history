package com.example.tansit;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class PieChartActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pie_chart);

        findViewById(R.id.buttonPieChart3months).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(getApplicationContext(), PieChartActivity3months.class));
            }
        });
        findViewById(R.id.buttonPieChart6months).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(getApplicationContext(), PieChartActivity6Months.class));
            }
        });


        PieChart pieChart = findViewById(R.id.pieChart);

        ArrayList<PieEntry> buses = new ArrayList<>();
        buses.add(new PieEntry(10, "B10"));
        buses.add(new PieEntry(20, "B11"));
        buses.add(new PieEntry(60, "B12"));
        buses.add(new PieEntry(50, "B13"));
        buses.add(new PieEntry(15, "B14"));


        PieDataSet pieDataSet = new PieDataSet(buses, "Buses");
        pieDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
        pieDataSet.setValueTextColor(Color.BLACK);
        pieDataSet.setValueTextSize(16f);

        PieData pieData = new PieData(pieDataSet);

        pieChart.setData(pieData);
        pieChart.getDescription().setEnabled(false);
        pieChart.setCenterText("Time taken by each bus in past journey");
        pieChart.animate();
    }
}