using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZedGraph;

namespace lab1_genetic
{
    public partial class Form1 : Form
    {
        public static List<all> ITEMS = new List<all>();
        public static IEnumerator<all> CARS;

        public Form1()
        {
            InitializeComponent();

            LoadData();
            //CARS = DB.alls.GetEnumerator();
            CARS = ITEMS.GetEnumerator();
            GetComboValues();
        }

        private void LoadData()
        {
            var streamReader = new StreamReader(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + "/data.txt");
            while (!streamReader.EndOfStream)
            {
                string line = streamReader.ReadLine();
                var lines = line.Split(',');

                var item = new all();
                item.name = lines[0];
                item.year = Convert.ToInt32(lines[1]);
                item.age = Convert.ToInt32(lines[2]);
                item.time = Convert.ToInt32(lines[3]);
                item.rating = Convert.ToDouble(lines[4], System.Globalization.CultureInfo.InvariantCulture);
                

                ITEMS.Add(item);
            }

            CARS = ITEMS.GetEnumerator();
        }

        private void GetComboValues()
        {
            var list = new List<ComboBox>();
            list.Add(cbCrit1);
            list.Add(cbCrit2);
            list.Add(cbCrit3);
            list.Add(cbCrit4);

            foreach (var cb in list)
            {
                cb.Items.Add("Год выпуска");
                cb.Items.Add("Продолжительность");
                cb.Items.Add("Возрастное ограничение");
                cb.Items.Add("Рейтинг");
            }

            cbCrit1.Text = "Год выпуска";
            cbCrit2.Text = "Продолжительность";
            cbCrit3.Text = "Возрастное ограничение";
            cbCrit4.Text = "Рейтинг";
        }

        void DrawGraphics(List<Input> input, all resultGA, all resultP)
        {
            // get a reference to the GraphPane
            GraphPane myPane = zgc.GraphPane;

            // Set the Titles
            myPane.Title.Text = "My Test Graph\n(For CodeProject Sample)";
            myPane.XAxis.Title.Text = "Порядковый номер фильма";
            myPane.YAxis.Title.Text = "Значение полезности (меньше-лучше)";
            myPane.CurveList.Clear();
            myPane.Title.IsVisible = false;
            myPane.XAxis.Title.IsVisible = true;
            myPane.YAxis.Title.IsVisible = true;

            //myPane.XAxis.Scale.Max = X;
            //myPane.YAxis.Scale.Max = Y;

            // Make up some data arrays based on the Sine function
            

            CARS = ITEMS.GetEnumerator();
            int i = 0;
            while (CARS.MoveNext())
            {
                var car = CARS.Current;

                PointPairList list = new PointPairList();
                list.Add(i, F(car, input));

                string title = "";
                var cl = Color.Lime;
                if (car == resultGA)
                {
                    title = "Фильм, выбранный генетическим алгоритмом";
                    cl = Color.Blue;
                }

                if (car == resultP)
                {
                    title = "Фильм, выбранный жадным алгоритмом";
                    cl = Color.Magenta;
                }

                var myCurve = myPane.AddCurve(title, list, cl, SymbolType.Circle);

                myCurve.Symbol.Fill = new Fill(cl);
                myCurve.Line.IsVisible = false;
                myCurve.Label.IsVisible = false;

                if ((car == resultP) || (car == resultGA))
                    myCurve.Label.IsVisible = true;

                i++;
            }
            

            // Set the Y axis intersect the X axis at an X value of 0.0
            myPane.YAxis.Cross = 0.0;
            // Turn off the axis frame and all the opposite side tics
            myPane.Chart.Border.IsVisible = false;
            myPane.XAxis.MajorTic.IsOpposite = false;
            myPane.XAxis.MinorTic.IsOpposite = false;
            myPane.YAxis.MajorTic.IsOpposite = false;
            myPane.YAxis.MinorTic.IsOpposite = false;

            // Calculate the Axis Scale Ranges
            zgc.AxisChange();
            zgc.Refresh();
        }

        public static double F(all car, List<Input> input)
        {
            double answer = 0;
            foreach (var inp in input)
            {
                if (inp.Mode)
                    answer += 1/GetValue(car, inp.Key, true)*inp.Value;
                else
                    answer += Math.Sqrt(GetValue(car, inp.Key, true) * inp.Value);
            }
            return answer;
        }

        public static double GetValue(all car, string cb, bool isMax)
        {
            switch (cb)
            {
                default:
                case "Год выпуска":
                    if (isMax) return car.year; else return year_max - car.year;
                case "Продолжительность":
                    if (isMax) return car.time; else return time_max - car.time;
                case "Возрастное ограничение":
                    if (isMax) return car.age; else return age_max - car.age;
                case "Рейтинг":
                    if (isMax) return car.rating; else return rating_max - car.rating;
                
            }
        }


        private const double time_max = 300;
        private const double year_max = 2016;
        private const double age_max = 19;
        private const double rating_max = 10;

        private void btnRun_Click(object sender, EventArgs e)
        {
            lblCName1.Text = cbCrit1.Text;
            lblCName2.Text = cbCrit2.Text;
            lblCName3.Text = cbCrit3.Text;
            lblCName4.Text = cbCrit4.Text;
            lblC1Name1.Text = cbCrit1.Text;
            lblC1Name2.Text = cbCrit2.Text;
            lblC1Name3.Text = cbCrit3.Text;
            lblC1Name4.Text = cbCrit4.Text;

            var input = new List<Input>();
            input.Add(new Input(cbCrit1.Text, (double)(nudCrit1.Value) / 100, cbCrit1Type.Text == "max"));
            input.Add(new Input(cbCrit2.Text, (double)(nudCrit2.Value) / 100, cbCrit2Type.Text == "max"));
            input.Add(new Input(cbCrit3.Text, (double)(nudCrit3.Value) / 100, cbCrit3Type.Text == "max"));
            input.Add(new Input(cbCrit4.Text, (double)(nudCrit4.Value) / 100, cbCrit4Type.Text == "max"));


            var resultGA = GetGenetic(input);
            var resultP = GetP(input);

            DrawGraphics(input, resultGA.Key, resultP.Key);
        }

        private KeyValuePair<all, double> GetP(List<Input> input)
        {
            var items = new List<KeyValuePair<all, double>>();
            //CARS = DB.alls.GetEnumerator();
            CARS = ITEMS.GetEnumerator();
            while (CARS.MoveNext())
            {
                var car = CARS.Current;
                items.Add(new KeyValuePair<all, double>(car, F(car, input)));
            }

            var P = new P(items, input);
            var answer = P.GetResult();

            lblP.Text = P.Time + " ms";
            lbl1Crit1.Text = GetValue(answer.Key, input[0].Key, true).ToString();
            lbl1Crit2.Text = GetValue(answer.Key, input[1].Key, true).ToString();
            lbl1Crit3.Text = GetValue(answer.Key, input[2].Key, true).ToString();
            lbl1Crit4.Text = GetValue(answer.Key, input[3].Key, true).ToString();

            lbl1CritName.Text = answer.Key.name;
            lblMark2.Text = Math.Round(answer.Value, 3).ToString();

            return answer;
        }

        private KeyValuePair<all, double> GetGenetic(List<Input> input)
        {
            var items = new List<KeyValuePair<all, double>>();
            //CARS = DB.alls.GetEnumerator();
            CARS = ITEMS.GetEnumerator();
            while (CARS.MoveNext())
            {
                var car = CARS.Current;
                items.Add(new KeyValuePair<all, double>(car, F(car, input)));
            }

            var GA = new GA(items, input);
            var answer = GA.GetResult();
            lblGA.Text = GA.Time + " ms";
            lblCrit1.Text = GetValue(answer.Key, input[0].Key, true).ToString();
            lblCrit2.Text = GetValue(answer.Key, input[1].Key, true).ToString();
            lblCrit3.Text = GetValue(answer.Key, input[2].Key, true).ToString();
            lblCrit4.Text = GetValue(answer.Key, input[3].Key, true).ToString();

            lblCritName.Text = answer.Key.name;
            lblMark1.Text = Math.Round(answer.Value, 3).ToString();
            return answer;
        }
    }

    public class Input
    {
        public string Key;
        public double Value;
        public bool Mode;

        public Input(string key, double value, bool mode)
        {
            Key = key;
            Value = value;
            Mode = mode;
        }
    }

}
