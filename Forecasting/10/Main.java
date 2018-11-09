import java.util.*;

public class Main {

    public static void main(String[] args) {
        long start=System.currentTimeMillis();

        try {
            Forecasting forecasting_10 = new Forecasting(500, 10);
            int lastInstance_10 = (int)forecasting_10.getData().lastInstance().value(0);
            Date date_10 = forecasting_10.getDateByID(lastInstance_10);
            Date[] dates_10 = new Date[forecasting_10.getTest_size()];

            Calendar cal_10 = Calendar.getInstance();
            cal_10.setTimeZone(TimeZone.getTimeZone("Europe/Warsaw"));
            cal_10.setTime(date_10);
            int min_10 = 3;
            for(int i =0; i< dates_10.length; i++){
                cal_10.add(Calendar.MINUTE, min_10);
                dates_10[i] = cal_10.getTime();
            }

            // temperatura - SVM / 4
            forecasting_10.create_a_Forecast("SVM", "temperatura",  4);
            double[] temp_10 = forecasting_10.getPrediction();

            // Wilgotność - SVM / 2
            forecasting_10.create_a_Forecast("SVM", "wilgotnosc",  2);
            double[] wilg_10 = forecasting_10.getPrediction();
            for(int i=0; i<wilg_10.length; i++){
                if (wilg_10[i]> 100){
                    wilg_10[i] = 100;
                }else if(wilg_10[i] < 0){
                    wilg_10[i]=0;
                }
            }

            // Ciśnienie - LinearRegression / 2
            forecasting_10.create_a_Forecast("LR", "cisnienie",  2);
            double[] cis_10 = forecasting_10.getPrediction();

            forecasting_10.setPredicitions( dates_10,temp_10,wilg_10,cis_10);
        } catch (Exception ex){
            System.out.println("Błąd!" + ex.getMessage() + " " + ex.getStackTrace()[0].getLineNumber());
        }
        long stop=System.currentTimeMillis();
        System.out.println("Czas wykonania: "+(stop-start)/1000 + " s");
        

    }



}
