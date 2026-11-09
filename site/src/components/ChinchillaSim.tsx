import { useMemo, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  buildLossCurves,
  chinchillaOptimalNd,
  dataWallCompute,
  effectiveTokens,
  formatParams,
  formatTokens,
  loss,
  lossPenaltyVsChinchilla,
  tokensUnderBudget,
} from "../lib/chinchilla";
import { Formula } from "./Formula";

export function ChinchillaSim() {
  const [logC, setLogC] = useState(25);
  const [logN, setLogN] = useState(11);
  const [logDHuman, setLogDHuman] = useState(14);
  const [synthRatio, setSynthRatio] = useState(1);
  const [quality, setQuality] = useState(0.6);

  const c = 10 ** logC;
  const n = 10 ** logN;
  const dHuman = 10 ** logDHuman;
  const dSynthetic = synthRatio * dHuman;

  const { n: nStar, d: dStar } = chinchillaOptimalNd(c);
  const dEff = effectiveTokens(dHuman, dSynthetic, quality);
  const dBudget = tokensUnderBudget(c, n);
  const dUsed = Math.min(dBudget, dEff);
  const regime = dBudget > dEff ? "DATA-CAP CONSTRAINED" : "Unconstrained Chinchilla";
  const lChin = loss(nStar, dStar);
  const lActual = loss(n, dUsed);
  const penalty = lossPenaltyVsChinchilla(lActual, lChin);

  const curve = useMemo(() => buildLossCurves(dEff), [dEff]);

  const wallLog = Math.log10(dataWallCompute(dEff));

  return (
    <div className="sim" id="sim-chinchilla">
      <div className="sim-controls">
        <h3 className="sim-title">Interactive laboratory</h3>
        <p className="sim-note">
          Adjust compute, parameters, and the synthetic mix. The amber curve
          diverges once unique effective tokens bind.
        </p>

        <label className="field">
          <span>
            Compute <Formula tex="C" /> (log₁₀ FLOPs)
            <em>{logC.toFixed(1)}</em>
          </span>
          <input
            type="range"
            min={23}
            max={28}
            step={0.1}
            value={logC}
            aria-label={`Compute budget C, log10 FLOPs, currently ${logC.toFixed(1)}`}
            onChange={(e) => setLogC(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Parameters <Formula tex="N" /> (log₁₀)
            <em>{logN.toFixed(2)}</em>
          </span>
          <input
            type="range"
            min={9}
            max={13}
            step={0.05}
            value={logN}
            aria-label={`Parameter count N, log10, currently ${logN.toFixed(2)}`}
            onChange={(e) => setLogN(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Human cap <Formula tex="D_{\mathrm{human}}" /> (log₁₀)
            <em>{logDHuman.toFixed(2)}</em>
          </span>
          <input
            type="range"
            min={12}
            max={15}
            step={0.05}
            value={logDHuman}
            aria-label={`Human token cap D_human, log10, currently ${logDHuman.toFixed(2)}`}
            onChange={(e) => setLogDHuman(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Synthetic mix <Formula tex="D_s / D_h" />
            <em>{synthRatio.toFixed(1)}×</em>
          </span>
          <input
            type="range"
            min={0}
            max={5}
            step={0.1}
            value={synthRatio}
            aria-label={`Synthetic to human token mix ratio, currently ${synthRatio.toFixed(1)}`}
            onChange={(e) => setSynthRatio(Number(e.target.value))}
          />
        </label>

        <label className="field">
          <span>
            Synthetic quality <Formula tex="\delta" />
            <em>{quality.toFixed(2)}</em>
          </span>
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={quality}
            aria-label={`Synthetic quality delta, currently ${quality.toFixed(2)}`}
            onChange={(e) => setQuality(Number(e.target.value))}
          />
        </label>
      </div>

      <div className="sim-stage">
        <div className="metric-row">
          <div className="metric">
            <span className="metric-label">Regime</span>
            <strong
              className={
                regime.startsWith("DATA") ? "metric-warn" : "metric-ok"
              }
            >
              {regime}
            </strong>
          </div>
          <div className="metric">
            <span className="metric-label">Allocated N</span>
            <strong>{formatParams(n)}</strong>
          </div>
          <div className="metric">
            <span className="metric-label">Effective D</span>
            <strong>{formatTokens(dEff)}</strong>
          </div>
          <div className="metric">
            <span className="metric-label">Loss penalty</span>
            <strong>{(penalty * 100).toFixed(2)}%</strong>
          </div>
        </div>

        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height={340}>
            <LineChart data={curve} margin={{ top: 12, right: 16, left: 0, bottom: 8 }}>
              <CartesianGrid stroke="rgba(154,167,181,0.12)" strokeDasharray="3 6" />
              <XAxis
                dataKey="logC"
                type="number"
                domain={[23, 28]}
                tick={{ fill: "#9aa7b5", fontSize: 12 }}
                label={{
                  value: "log₁₀ compute (FLOPs)",
                  position: "insideBottom",
                  offset: -2,
                  fill: "#9aa7b5",
                }}
              />
              <YAxis
                tick={{ fill: "#9aa7b5", fontSize: 12 }}
                domain={["auto", "auto"]}
                label={{
                  value: "Predicted loss L",
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
                labelFormatter={(v) => `log₁₀ C = ${Number(v).toFixed(2)}`}
              />
              <Legend />
              <ReferenceLine
                x={Math.min(28, Math.max(23, wallLog))}
                stroke="#9aa7b5"
                strokeDasharray="4 6"
                label={{ value: "wall", fill: "#9aa7b5", fontSize: 11 }}
              />
              <Line
                type="monotone"
                dataKey="unconstrained"
                name="Unconstrained Chinchilla"
                stroke="#5ec4a8"
                strokeWidth={2}
                dot={false}
                strokeDasharray="6 4"
              />
              <Line
                type="monotone"
                dataKey="capped"
                name="Data-capped actual"
                stroke="#e0a45a"
                strokeWidth={2.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <p className="sim-footer">
          Chinchilla optimum at this <Formula tex="C" />:{" "}
          <Formula tex="N^\star" /> ≈ {formatParams(nStar)},{" "}
          <Formula tex="D^\star" /> ≈ {formatTokens(dStar)}. Raising{" "}
          <Formula tex="\delta" /> (PRM / compiler filtering) shifts the wall
          rightward without inventing infinite human text.
        </p>
      </div>
    </div>
  );
}
