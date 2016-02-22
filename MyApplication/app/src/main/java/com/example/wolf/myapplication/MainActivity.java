package com.example.wolf.myapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    int i = 0;
    float c = 40;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void buttonOnClick(View v) {
        Button button = (Button) v;
        if (button.getText().equals("Hope?")) {
            button.setText("Yes there is...");
        } else {
            button.setTextSize(c += 5);
            button.setText(Integer.toString(i));

            i++;

        }

// do something when the button is clicked
    }
}
