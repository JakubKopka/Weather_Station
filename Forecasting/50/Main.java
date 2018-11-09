import java.util.*;

public class Main {

    public static void main(String[] args) {
        long start=System.currentTimeMillis();

        try {

            Forecasting forecasting_50 = new Forecasting(500, 50);
            int lastInstance_50 = (int)forecasting_50.getData().lastInstance().value(0);
            Date date_50 = forecasting_50.getDateByID(lastInstance_50);
            Date[] dates_50 = new Date[forecasting_50.getTest_size()];

            Calendar cal_50 = Calendar.getInstance();
            cal_50.setTimeZone(TimeZone.getTimeZone("Europe/Warsaw"));
            cal_50.setTime(date_50);
            int min_50 = 3;
            for(int i =0; i< dates_50.length; i++){
                cal_50.add(Calendar.MINUTE, min_50);
                dates_50[i] = cal_50.getTime();
            }

            System.out.println("============ Daty ==============");
            for (int i =0; i<forecasting_50.getTest_size(); i++){
                System.out.println(dates_50[i]);
            }



            // temperatura - SVM / 4
            forecasting_50.create_a_Forecast("SVM", "temperatura",  4);
            double[] temp_50 = forecasting_50.getPrediction();
            System.out.println("============Temperatura===========");
            for(int i = 0; i< temp_50.length; i++){
                System.out.println(temp_50[i]);
            }
            System.out.println("========================================");


            // Wilgotność - SVM / 4
            forecasting_50.create_a_Forecast("SVM", "wilgotnosc",  4);
            double[] wilg_50 = forecasting_50.getPrediction();
            System.out.println("============Wilgotnosc===========");
            for(int i = 0; i< wilg_50.length; i++){
                if (wilg_50[i]> 100){
                    wilg_50[i] = 100;
                }else if(wilg_50[i] < 0){
                    wilg_50[i]=0;
                }
            }
            System.out.println("========================================");


            // Ciśnienie - SVM / 1
            forecasting_50.create_a_Forecast("SVM", "cisnienie",  1);
            double[] cis_50 = forecasting_50.getPrediction();
            System.out.println("============Cisnienie===========");
            for(int i = 0; i< cis_50.length; i++){
                System.out.println(cis_50[i]);
            }
            System.out.println("========================================");

            forecasting_50.setPredicitions(dates_50,temp_50,wilg_50,cis_50);
        } catch (Exception ex){
            System.out.println("Błąd!" + ex.getMessage() + " " + ex.getStackTrace()[0].getLineNumber());
        }
        long stop=System.currentTimeMillis();
        System.out.println("Czas wykonania: "+(stop-start)/1000 + " s");
        

    }



}
