import java.io.File;

import java.io.PrintWriter;
import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JPanel;

import org.omg.Messaging.SYNC_WITH_TRANSPORT;
import weka.classifiers.functions.GaussianProcesses;
import weka.classifiers.functions.LinearRegression;
import weka.classifiers.functions.supportVector.Kernel;
import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;

import weka.classifiers.functions.SMOreg;
import weka.classifiers.evaluation.NumericPrediction;
import weka.classifiers.timeseries.WekaForecaster;
import weka.classifiers.timeseries.eval.TSEvaluation;
import weka.classifiers.timeseries.eval.graph.JFreeChartDriver;
import weka.core.stopwords.Null;
import weka.experiment.InstanceQuery;
import weka.classifiers.functions.GaussianProcesses;

public class Forecasting {

    private Instances data;
    private  int train_size;
    private int test_size;
    private double[] prediction;
    private String DB_URL = "jdbc:mysql://54.37.138.103:3306/PracaLicencjacka?autoReconnect=true&useSSL=false";
    private Connection conn = null;
    private Statement stmt = null;
    private String user="";
    private String passwd="";
    String host="";
    String db="";
    String port = "";

    public Instances getData() {
        return data;
    }

    public int getTrain_size() {
        return train_size;
    }

    public int getTest_size() {
        return test_size;
    }

    public double[] getPrediction() {
        return prediction;
    }


    public Forecasting(int train_size, int test_size) throws Exception{
        this.test_size = test_size;
        this.train_size = train_size;

//        int d = this.train_size + this.test_size +1;
        InstanceQuery query = new InstanceQuery();
        query.setDatabaseURL("jdbc:mysql://54.37.138.103:3306/PracaLicencjacka?autoReconnect=true&useSSL=false");
        query.setUsername(this.user);
        query.setPassword(this.passwd);
        // do 13586 - fajne odczyty z dnia 07.04.2018
        String query_sql = String.format("SELECT * FROM stacjapogodowa_odczyty WHERE stacjapogodowa_odczyty.id > " +
                "(SELECT MAX(stacjapogodowa_odczyty.id) - %d FROM stacjapogodowa_odczyty)",this.train_size);
        query.setQuery(query_sql);
//        query.setQuery("SELECT * FROM stacjapogodowa_odczyty WHERE stacjapogodowa_odczyty.id > (SELECT MAX(stacjapogodowa_odczyty.id) - %d FROM stacjapogodowa_odczyty)", data);
//        query.setQuery("SELECT * FROM stacjapogodowa_odczyty where stacjapogodowa_odczyty.id > 8949 and stacjapogodowa_odczyty.id <= 9500");
        this.data = query.retrieveInstances();
        System.out.println(this.data.lastInstance());


    }

    public Date getDateByID(int id)throws Exception{
        //stacjapogodowa_odczyty.data_odczytu
        String query_sql = String.format("SELECT * FROM stacjapogodowa_odczyty WHERE stacjapogodowa_odczyty.id=%d",id);


        //  parametry bazy danych

        Date date = new Date();
        try{
            // Połączenie z bazą danych
            System.out.println("Connecting to database...");
            conn = DriverManager.getConnection(DB_URL,user,passwd);

            // Stworzenie zapytania oraz jego wykonanie
            System.out.println("Creating statement...");
            this.stmt = this.conn.createStatement();
            String sql;

            ResultSet rs = this.stmt.executeQuery(query_sql);

            // Ekstrakcja wyników
            while(rs.next()){
                //Retrieve by column name
                date = rs.getTimestamp("data_odczytu");
            }
            // Czyszczenie po sobie
            rs.close();
            this.stmt.close();
            this.conn.close();
        }catch(SQLException se){
            //Errory JDBC
            se.printStackTrace();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            //finally block - by pozamykać resources
            try{
                if(this.stmt!=null)
                    this.stmt.close();
            }catch(SQLException se2){
            }// nothing we can do
            try{
                if(this.conn!=null)
                    this.conn.close();
            }catch(SQLException se){
                se.printStackTrace();
            }//end finally try
        }//end try

        return date;

    }

    public void setPredicitions(Date[] dates, double[] temp, double[] wilg, double[] cis)throws Exception {
        try {
            System.out.println("Connecting to a selected database...");
            this.conn = DriverManager.getConnection(this.DB_URL, this.user, this.passwd);
            System.out.println("Connected database successfully...");

            System.out.println("Inserting records into the table...");
            this.stmt = this.conn.createStatement();

            for (int i =0; i<dates.length; i++){
                String formattedDate = new SimpleDateFormat("yyyy-MM-dd HH:mm").format(dates[i]);
                PreparedStatement stmt;
                if(dates.length == 50){
                    stmt  = conn.prepareStatement(
                            "INSERT INTO stacjapogodowa_odczyty_50 ( data_odczytu, temperatura, wilgotnosc, cisnienie) " +
                                    " values (?, ?, ?, ? )");
                }else{
                    stmt  = conn.prepareStatement(
                            "INSERT INTO stacjapogodowa_odczyty_10 ( data_odczytu, temperatura, wilgotnosc, cisnienie) " +
                                    " values (?, ?, ?, ? )");
                }

                stmt .setString( 1, formattedDate);
                stmt .setString( 2, Double.toString(temp[i]) );
                stmt .setString( 3, Double.toString(wilg[i]) );
                stmt .setString( 4, Double.toString(cis[i]));

                stmt.executeUpdate();
                System.out.println(formattedDate + " " + temp[i]+ " " + wilg[i]  +" " + cis[i]);
            }

        } catch (SQLException se) {
            //Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            //Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            //finally block used to close resources
            try {
                if (this.stmt != null)
                    this.conn.close();
            } catch (SQLException se) {
            } // do nothing
            try {
                if (this.conn != null)
                    this.conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            } //end finally try
        } //end try
    }

    public void create_a_Forecast(String model, String label, int window_size){
        double[] truth = new double[this.test_size];
        this.prediction = new double[this.test_size];

        int start_idx=0;
        double[] abs = new double[this.test_size];

        Instances train = new Instances(this.data, start_idx, this.train_size);
//        Instances test = new Instances(this.data, start_idx + train_size + 1, test_size);

        WekaForecaster forecaster = new WekaForecaster();
        try{
            forecaster.setFieldsToForecast(label);
        }catch (Exception ex){
            System.out.println("Błąd! Linia: "+  ex.getStackTrace()[0].getLineNumber());
        }

        SMOreg svm_reg = new SMOreg();

        if (model == "SVM"){// SVM
            forecaster.setBaseForecaster(svm_reg);
        }else if(model == "LR"){// LinearRegression
            forecaster.setBaseForecaster(new LinearRegression());
        }else if(model == "GP"){// GaussianProcesses
            forecaster.setBaseForecaster(new GaussianProcesses());
        }

        forecaster.getTSLagMaker().setMinLag(1);
        forecaster.getTSLagMaker().setMaxLag(this.test_size * window_size);
        forecaster.getTSLagMaker().setTimeStampField("id");

        try{
            forecaster.buildForecaster(train, System.out);
        }catch (Exception ex){
            System.out.println("Błąd! Linia: "+  ex.getStackTrace()[0].getLineNumber());
        }
        try{
            forecaster.primeForecaster(train);
        }catch (Exception ex){
            System.out.println("Błąd" + ex.toString() + "Linia: "+  ex.getStackTrace()[0].getLineNumber());
        }




        List<List<NumericPrediction>> forecast;

        try{
            forecast = forecaster.forecast(test_size, System.out);
            for (int i = 0; i < test_size; i++) {
                List<NumericPrediction> predsAtStep = forecast.get(i);
                double predicted = predsAtStep.get(0).predicted();
                double predicted_round = Math.round(predicted * 1000.0) / 1000.0;

//                double actual = test.instance(i).value(test.attribute(label));
//                double actual_round = Math.round(actual * 1000.0) / 1000.0;

//                double abs_diff = Math.abs(predicted - actual);
//                double abs_diff_round = Math.round(abs_diff * 10000.0) / 10000.0;
//                truth[i] = actual_round;
                this.prediction[i] = predicted_round;
//                abs[i] = abs_diff_round;

            }
        }catch (Exception ex){
            System.out.println("Błąd! Linia: "+  ex.getStackTrace()[0].getLineNumber());
        }

    }

}
