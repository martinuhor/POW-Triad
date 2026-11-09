import { useMemo, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { simulatePaths } from "../lib/gdp";
import { Formula } from "./Formula";

export function GdpSim() {
  const [exposurePct, setExposurePct] = useState(40);
  const [easySharePct, setEasySharePct] = useState(60);
  const [savingsEasy, setSavingsEasy] = useState(0.25);
  const [savingsHard, setSavingsHard] = useState(0.1);
  const [halfEasy, setHalfEasy] = useState(2);
  const [halfHard, setHalfHard] = useState(6);
  const [capitalDrag, setCapitalDrag] = useState(0.45);

  const rows = useMemo(
    () =>
      simulatePaths({
        exposure: exposurePct / 100,
        savingsEasy,
        savingsHard,
        easyShare: easySharePct / 100,
        adoptionHalflifeEasy: halfEasy,
        adoptionHalflifeHard: halfHard,
        capitalDrag,
      }),
    [
      exposurePct,
      easySharePct,
      savingsEasy,
      savingsHard,
      halfEasy,
      halfHard,
      capitalDrag,
    ],
  );

  const y10 = rows[rows.length - 1];
  const lagPp = 100 * (y10.gdpDigitalOnly - y10.gdp);

  return (
    <div className="sim" id="sim-gdp">
      <div className="sim-controls">
        <h3 className="sim-title">Interactive laboratory</h3>
        <p className="sim-note">
          Task exposure and adoption speed set the TFP path. Capital drag
          decides how much of that path shows up in GDP.
        </p>

        <label className="field">
          <span>
            Task exposure
            <em>{exposurePct.toFixed(0)}%</em>
          </span>
          <input
            type="range"
            min={0}
            max={100}
            step={1}
            value={exposurePct}
            onChange={(e) => setExposurePct(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Easy share of exposed tasks
            <em>{easySharePct.toFixed(0)}%</em>
          </span>
          <input
            type="range"
            min={0}
            max={100}
            step={1}
            value={easySharePct}
            onChange={(e) => setEasySharePct(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Cost savings — easy
            <em>{(savingsEasy * 100).toFixed(0)}%</em>
          </span>
          <input
            type="range"
            min={0}
            max={0.5}
            step={0.01}
            value={savingsEasy}
            onChange={(e) => setSavingsEasy(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Cost savings — hard
            <em>{(savingsHard * 100).toFixed(0)}%</em>
          </span>
          <input
            type="range"
            min={0}
            max={0.5}
            step={0.01}
            value={savingsHard}
            onChange={(e) => setSavingsHard(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Easy adoption half-life
            <em>{halfEasy.toFixed(1)} yr</em>
          </span>
          <input
            type="range"
            min={0.5}
            max={8}
            step={0.5}
            value={halfEasy}
            onChange={(e) => setHalfEasy(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Hard adoption half-life
            <em>{halfHard.toFixed(1)} yr</em>
          </span>
          <input
            type="range"
            min={0.5}
            max={12}
            step={0.5}
            value={halfHard}
            onChange={(e) => setHalfHard(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Physical capital drag
            <em>{(capitalDrag * 100).toFixed(0)}%</em>
          </span>
          <input
            type="range"
            min={0}
            max={0.9}
            step={0.05}
            value={capitalDrag}
            onChange={(e) => setCapitalDrag(Number(e.target.value))}
          />
        </label>
      </div>

      <div className="sim-stage">
        <div className="metric-row">
          <div className="metric">
            <span className="metric-label">Year-10 TFP</span>
            <strong>
              {y10.tfp.toFixed(3)}{" "}
              <small>+{y10.tfpGrowthCumPct.toFixed(1)}%</small>
            </strong>
          </div>
          <div className="metric">
            <span className="metric-label">Year-10 GDP</span>
            <strong>
              {y10.gdp.toFixed(3)}{" "}
              <small>+{y10.gdpGrowthCumPct.toFixed(1)}%</small>
            </strong>
          </div>
          <div className="metric">
            <span className="metric-label">Digital-only GDP</span>
            <strong>{y10.gdpDigitalOnly.toFixed(3)}</strong>
          </div>
          <div className="metric">
            <span className="metric-label">GDP lag vs digital</span>
            <strong className="metric-warn">{lagPp.toFixed(1)} pp</strong>
          </div>
        </div>

        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height={340}>
            <LineChart data={rows} margin={{ top: 12, right: 16, left: 0, bottom: 8 }}>
              <CartesianGrid stroke="rgba(154,167,181,0.12)" strokeDasharray="3 6" />
              <XAxis
                dataKey="year"
                tick={{ fill: "#9aa7b5", fontSize: 12 }}
                label={{
                  value: "Years post-deployment",
                  position: "insideBottom",
                  offset: -2,
                  fill: "#9aa7b5",
                }}
              />
              <YAxis
                tick={{ fill: "#9aa7b5", fontSize: 12 }}
                domain={["auto", "auto"]}
                label={{
                  value: "Index (year 0 = 1)",
                  angle: -90,
                  position: "insideLeft",
                  fill: "#9aa7b5",
                }}
              />
              <Tooltip
                contentStyle={{
                  background: "#0e1319",
                  border: "1px solid rgba(154,167,181,0.25)",
                  borderRadius: 8,
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="tfp"
                name="TFP"
                stroke="#5ec4a8"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="gdpDigitalOnly"
                name="GDP (digital-only)"
                stroke="#8fd4c1"
                strokeWidth={2}
                strokeDasharray="6 4"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="gdp"
                name="GDP (with capital drag)"
                stroke="#e0a45a"
                strokeWidth={2.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <p className="sim-footer">
          Measured GDP = <Formula tex="\exp\!\big(\log\mathrm{TFP}\cdot(1-\kappa)\big)" />{" "}
          where <Formula tex="\kappa" /> is physical capital / deployment drag.
          Internal lab capability can track the teal path while the economy
          tracks amber.
        </p>
      </div>
    </div>
  );
}
