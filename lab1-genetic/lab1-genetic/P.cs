using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace lab1_genetic
{
    public class P
    {
        public List<KeyValuePair<all, double>> items = new List<KeyValuePair<all, double>>();
        public List<Input> input = new List<Input>();
        private Stopwatch SW = new Stopwatch();
        public double Time = 0;

        public P(List<KeyValuePair<all, double>> items, List<Input> input)
        {
            var idx = input.IndexOf(input.OrderByDescending(el => el.Value).First());
            if(!input[idx].Mode)
                items = items.OrderBy(i => GetValue(i.Key, input[idx].Key)).ToList();
            else
                items = items.OrderByDescending(i => GetValue(i.Key, input[idx].Key)).ToList();
           
            this.items = items;
            this.input = input;
        }

        public KeyValuePair<all, double> GetResult()
        {
            var answer = new KeyValuePair<all, double>(items[0].Key, items[0].Value);
            SW.Start();

            var car = items[0];
            var idx = input.IndexOf(input.OrderByDescending(el => el.Value).First());

            for (int i = 0; i < items.Count; i++)
            {
                var sett = new List<double>();

                if (idx == 0)
                    sett.Add(GetValue(car.Key, input[0].Key));
                else
                    sett.Add(GetValue(items[i].Key, input[0].Key));

                    if (idx == 1)
                        sett.Add(GetValue(car.Key, input[1].Key));
                    else
                    sett.Add(GetValue(items[i].Key, input[1].Key));

                for (int j = 0; j < items.Count; j++)
                {
                    if (idx == 2)
                        sett.Add(GetValue(car.Key, input[2].Key));
                    else
                        sett.Add(GetValue(items[j].Key, input[2].Key));

                    for (int k = 0; k < items.Count; k++)
                    {
                        if (idx == 3)
                            sett.Add(GetValue(car.Key, input[3].Key));
                        else
                            sett.Add(GetValue(items[k].Key, input[3].Key));


                        var new_car = SetValues(car.Key, sett);

                        double value = Form1.F(new_car, input);
                        if (value < answer.Value)
                            answer = new KeyValuePair<all, double>(new_car, value);
                    }
                }
            }

            SW.Stop();
            Time = SW.Elapsed.TotalMilliseconds;

            return GetLocal(answer);
        }

        private KeyValuePair<all, double> GetLocal(KeyValuePair<all, double> car)
        {
            double value = car.Value;
            double p = (value / 100) * 25;

            var res =
                items.Select(el => el)
                    .Where(el => el.Value > value - p && el.Value < value + p)
                    .ToList()
                    .OrderBy(el => el.Value);

            return res.First();
        }

        public double GetValue(all car, string cb)
        {
            switch (cb)
            {
                default:
                case "Год выпуска":
                    return car.year;
                    break;
                case "Продолжительность":
                    return car.time;
                    break;
                case "Возрастное ограничение":
                    return car.age;
                    break;
                case "Рейтинг":
                    return car.rating;
                    break;
                
            }
        }


        private all SetValues(all car, List<double> sett)
        {
            car = new all();

            var values = sett;
            foreach (var inp in input)
            {
                int idx = input.IndexOf(inp);
                switch (inp.Key)
                {
                    default:
                    case "Год выпуска":
                        car.year = (int)values[idx];
                        break;
                    case "Продолжительность":
                        car.time = (int)values[idx];
                        break;
                    case "Возрастное ограничение":
                        car.age = (int)values[idx];
                        break;
                    case "Рейтинг":
                        car.rating = values[idx];
                        break;
                }
            }

            return car;
        }
    }
}
