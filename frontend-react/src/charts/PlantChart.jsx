import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
} from "recharts";

export default function PlantChart({ data }) {

  return (

    <ResponsiveContainer
      width="100%"
      height={350}
    >

      <BarChart data={data}>

        <XAxis dataKey="plant" />

        <YAxis />

        <Tooltip />

        <Bar
          dataKey="count"
          fill="#1976d2"
        />

      </BarChart>

    </ResponsiveContainer>

  );

}