using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lab1_genetic
{
    public class GA
    {
        public List<KeyValuePair<all, double>> items = new List<KeyValuePair<all, double>>();
        public List<Input> input = new List<Input>();
        private Random rnd = new Random(1);
        private Stopwatch SW = new Stopwatch();
        public double Time = 0;

        public GA(List<KeyValuePair<all, double>> items, List<Input> input)
        {
            items = items.OrderBy(i => GetValue(i.Key, input[0].Key)).ToList();
            this.items = items;
            this.input = input;
        }

        public KeyValuePair<all, double> GetResult()
        {
            SW.Start();
            var answer = new KeyValuePair<all, double>();

            var parent1 = items[rnd.Next(items.Count)];
            var parent2 = items[rnd.Next(items.Count)];

            int k = 0;
            while (k < 50)
            {
                var CHILDS = new List<KeyValuePair<all, double>>();
                CHILDS.Add(GetChild(parent1, parent2, 0, 2));
                CHILDS.Add(GetChild(parent1, parent2, 0, 1));
                CHILDS.Add(GetChild(parent1, parent2, 0, 0));

                CHILDS.Add(GetChild(parent1, parent2, 1, 3));
                CHILDS.Add(GetChild(parent1, parent2, 1, 2));
                CHILDS.Add(GetChild(parent1, parent2, 1, 1));

                CHILDS.Add(GetChild(parent1, parent2, 2, 3));
                CHILDS.Add(GetChild(parent1, parent2, 2, 2));

                CHILDS.Add(GetChild(parent1, parent2, 3, 3));

                CHILDS = CHILDS.OrderBy(el => Form1.F(el.Key, input)).ToList();
                
                var child1 = GetMutant(CHILDS[0]);
                var child2 = GetMutant(CHILDS[1]);
                
                answer = child1;

                if((child1.Value > parent1.Value) || (child1.Value > parent2.Value))
                    child1 = items[rnd.Next(items.Count)];

                if ((child2.Value > parent1.Value) || (child2.Value > parent2.Value))
                    child2 = items[rnd.Next(items.Count)];

                if (child1.Value == child2.Value)
                    break;

                parent1 = child1;
                parent2 = child2;

                k++;
            }
            SW.Stop();
            Time = SW.Elapsed.TotalMilliseconds;
            return answer;
        }

        private KeyValuePair<all, double> GetMutant(KeyValuePair<all, double> car)
        {
            double value = car.Value;
            double p = (value/100)*5;

            var res =
                items.Select(el => el)
                    .Where(el => el.Value > value - p && el.Value < value + p)
                    .ToList()
                    .OrderBy(el => el.Value);

            if (res.Any())
                return res.First();

            return items[rnd.Next(items.Count)];
        }

        private KeyValuePair<all, double> GetChild(KeyValuePair<all, double> parent1, KeyValuePair<all, double> parent2, int child_num_min, int child_num_max)
        {
            var sett = new List<double>();
            for (int i = 0; i < input.Count; i++)
            {
                if((i >= child_num_min) && (i <= child_num_max))
                    sett.Add(GetValue(parent1.Key, input[i].Key));
                else
                    sett.Add(GetValue(parent2.Key, input[i].Key));
            }

            var child = SetValues(parent1.Key, sett);
            return new KeyValuePair<all, double>(child, Form1.F(child, input));
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
