import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy import signal

# 初期パラメータの設定
Fs = 1000.0         # サンプリング周波数 [Hz]
Ts = 1.0 / Fs       # サンプリング周期 [s]
initial_fc = 50.0   # 初期カットオフ周波数 [Hz]
initial_taps = 51   # 初期タップ数（奇数）


def calc_filter(fc, num_taps):
  '''フィルタ計算およびシミュレーション用関数'''
  # 初期化処理
  if num_taps % 2 == 0:
    num_taps += 1   # タップ数が偶数の場合は奇数に補正

  N_half = (num_taps - 1) // 2  # 念のため端数切捨て
  fc_norm = fc / Fs             # カットオフ周波数の正規化

  n = np.arange(-N_half, N_half + 1)        # データ番号n
  h_ideal = np.zeros_like(n, dtype=float)   # 理想ローパスフィルタのインパルス応答値格納用配列h_idealの初期化

  # 理想ローパスフィルタのインパルス応答 h_ideal(n) の計算（n=0時の例外処理込み）
  for i, val in enumerate(n):
    if val == 0:
      h_ideal[i] = 2.0 * fc_norm
    else:
      h_ideal[i] = np.sin(2.0 * np.pi * fc_norm * val) / (np.pi * val)

  window = np.hamming(num_taps)     # ハミング窓データの生成
  h_fir = h_ideal * window          # ハミング窓の適用
  h_fir = h_fir / np.sum(h_fir)     # フィルタのDCゲインを厳密に0dBにするための正規化

  w, h_resp = signal.freqz(h_fir, 1.0, worN=1024, fs=Fs)    # 周波数特性の計算
  gain_db = 20 * np.log10(np.abs(h_resp))                   # ゲイン単位を[dB]に変換
  phase_deg = np.unwrap(np.angle(h_resp)) * (180 / np.pi)   # 位相単位を[deg]に換算

  t_end = 1.0                   # シミュレーション時間の指定
  t = np.arange(0, t_end, Ts)   # 時間データの生成
  u_signal = np.zeros_like(t)   # フィルタ入力信号用配列の初期化

  idx_start = int(round(0.3 / Ts))
  idx_end = int(round(0.7 / Ts))
  u_signal[idx_start:idx_end] = np.linspace(0, 1, idx_end - idx_start)  # 入力信号u(idx_startからidx_endまでランプ状に増大)

  np.random.seed(0)                                     # ランダムノイズ元データの生成
  u_noisy = u_signal + 0.03 * np.random.randn(len(t))   # ノイズレベルを調節して入力信号へ足し込み

  y_normal = signal.lfilter(h_fir, 1.0, u_noisy)        # FIRフィルタ処理による出力信号生成
  y_zerophase = signal.filtfilt(h_fir, 1.0, u_noisy)    # 零位相フィルタ処理による出力信号生成

  return w, gain_db, phase_deg, t, u_noisy, y_normal, y_zerophase, num_taps


# グラフの初期描画設定
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

# 初回データの取得とプロット
w, gain_db, phase_deg, t, u_noisy, y_normal, y_zerophase, current_taps = (
    calc_filter(initial_fc, initial_taps)
)

# 左上：周波数特性（ゲイン）
(line_gain,) = axes[0, 0].plot(w, gain_db, color="blue", lw=1.5)
axes[0, 0].set_ylabel("Gain[dB]",fontsize=8)
axes[0, 0].set_title(
    f"FIR Lowpass Filter (Hamming Window, Taps={current_taps}, fc={initial_fc}Hz)"
,fontsize=9)
axes[0, 0].tick_params(axis="both", labelsize=7)
axes[0, 0].grid(True, which="both", ls="--")
axes[0, 0].set_xscale("log")
axes[0, 0].set_ylim([-100, 10])
axes[0, 0].set_xlim([1, 0.5*Fs])

# 左下：周波数特性（位相）
(line_phase,) = axes[1, 0].plot(w, phase_deg, color="blue", lw=1.5)
axes[1, 0].set_ylabel("Phase[deg]",fontsize=8)
axes[1, 0].set_xlabel("Frequency[Hz]",fontsize=8)
axes[1, 0].tick_params(axis="both", labelsize=7)
axes[1, 0].grid(True, which="both", ls="--")
axes[1, 0].set_xscale("log")
axes[1, 0].set_xlim([1, 0.5*Fs])

# 右上：時間応答の比較（通常のFIRフィルタと零位相フィルタ）
axes[0, 1].plot(t, u_noisy, label="Noisy Input", color="blue", linewidth=1, alpha=0.3)
(line_normal,) = axes[0, 1].plot(t, y_normal, label="Normal Filter", color="crimson", linestyle="--", linewidth=1, alpha=0.9)
(line_zerophase,) = axes[0, 1].plot(t, y_zerophase, label="Zero-Phase Filter", color="green", linewidth=1.5, alpha=1.0)
axes[0, 1].set_xlabel("Time [s]",fontsize=8)
axes[0, 1].set_ylabel("Amplitude [-]",fontsize=8)
axes[0, 1].set_title("Comparison of Normal Filter and Zero-Phase Filter",fontsize=9)
axes[0, 1].tick_params(axis="both", labelsize=7)
axes[0, 1].grid(True, linestyle="--")
axes[0, 1].legend(fontsize=8)

# 右下：スライダー
axes[1, 1].axis("off")  # スライダー表示のため目盛りをOFF



# スライダーの配置と更新イベントの定義
ax_fc = plt.axes([0.60, 0.30, 0.25, 0.05])      # カットオフ周波数設定スライダーの描画エリア（[left, bottom, width, height]）
ax_taps = plt.axes([0.60, 0.20, 0.25, 0.05])    # タップ数設定スライダーの描画エリア（[left, bottom, width, height]）

slider_fc = Slider(
    ax_fc,
    "Cutoff[Hz]",
    1.0,
    500.0,
    valinit=initial_fc,
    valstep=10.0,
)
slider_taps = Slider(
    ax_taps,
    "Taps[-]",
    1,
    101,
    valinit=initial_taps,
    valstep=1,
)


def update(val):
  '''グラフ更新用関数'''
  fc_val = slider_fc.val
  taps_val = int(slider_taps.val)

  # フィルタ再計算および再シミュレーション
  w, gain_db, phase_deg, t, u_noisy, y_normal, y_zerophase, current_taps = (
      calc_filter(fc_val, taps_val)
  )

  # グラフのデータを更新
  line_gain.set_ydata(gain_db)
  line_phase.set_ydata(phase_deg)
  line_normal.set_ydata(y_normal)
  line_zerophase.set_ydata(y_zerophase)

  axes[0, 0].set_title(
      f"FIR Lowpass Filter (Hamming Window, Taps={current_taps}, fc={fc_val}Hz)"
      ,fontsize=9
  )

  fig.canvas.draw_redraw()


# スライダーの値が変更されたときupdate関数を呼び出し
slider_fc.on_changed(update)
slider_taps.on_changed(update)

plt.show()