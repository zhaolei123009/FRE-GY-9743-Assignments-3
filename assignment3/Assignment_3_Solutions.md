# FRE-GT-9743 Assignment 3: Solutions

## Assumptions and conventions

Prices are quoted per $100 face value. The bond pays regular semiannual coupons and has exactly nine years remaining, so the valuation date is treated as immediately after a coupon payment. Initial accrued interest is therefore zero, and the next coupon is paid in six months.

Because no calendar dates or repo day-count convention are specified, three months is taken as 0.25 years and repo interest is calculated on a simple-interest basis. The 6% reference yield is a nominal annual yield compounded semiannually.

The conversion factor is calculated from the bond's current nine-year remaining cashflows, as defined in the assignment. This convention reproduces the futures quote in Question 2. Actual exchange conversion factors follow contract-specific reference-date and rounding rules.

## 1. Normalized forward price

### 1.1 Three-month forward price

Each semiannual coupon equals

$$C=100\times\frac{0.04}{2}=2.$$

No coupon is paid during the three-month holding period. Buying the bond for $100 and financing it at a 2% repo rate creates a repayment obligation at delivery of

$$P_{\mathrm{forward}}^{\mathrm{dirty}}=100(1+0.02\times0.25)=100.5.$$

At delivery, accrued interest equals half of a semiannual coupon:

$$AI(T)=2\times\frac{3}{6}=1.$$

The clean forward price is therefore

$$\boxed{BF=100.5-1=99.5.}$$

The distinction between clean and dirty prices matters: the delivery invoice includes accrued interest separately, so the price normalized by the conversion factor must be the clean forward price.

### 1.2 Conversion factor

There are $9\times2=18$ remaining coupon payments. At a 6% nominal annual yield, the discount rate per half-year is 3%. The reference price is

$$P_{6\%}=\sum_{i=1}^{18}\frac{2}{1.03^i}+\frac{100}{1.03^{18}}
=2\frac{1-1.03^{-18}}{0.03}+100(1.03)^{-18}
=86.24648692.$$

Initial accrued interest is zero, so this is also the clean reference price. Consequently,

$$\boxed{K=\frac{P_{6\%}}{100}=0.8624648692.}$$

### 1.3 Normalized forward price

$$\boxed{\frac{BF}{K}=\frac{99.5}{0.8624648692}
=115.3670179\approx115.3670.}$$

### 1.4 Interpretation of the conversion factor

Deliverable bonds differ in coupon and maturity. The conversion factor provides a common price benchmark by valuing each bond at the same 6% reference yield. A bond with a coupon below 6% generally has a reference price below par and a conversion factor below one; a bond with a coupon above 6% generally has a factor above one.

At the conversion-factor reference date, the definition implies

$$\frac{P_{6\%,x}^{\mathrm{clean}}}{K_x}=100.$$

The delivery invoice for bond $x$ is

$$\text{Invoice}_x=F K_x+AI_x(T).$$

Thus, the factor adjusts the clean-price component for differences in contractual cashflows, while accrued interest is paid separately. It does not eliminate differences in duration, convexity, financing costs, or holding-period coupon income. Those differences allow one bond to be cheaper to deliver than another.

## 2. Cheapest-to-deliver bond

### 2.1 Implied repo rate

For this bond there are no coupon payments before delivery. The implied repo rate is the financing rate that makes buying the bond and delivering it against the futures contract break even:

$$100(1+r_{\mathrm{imp}}\times0.25)=F K+AI(T).$$

Solving for the rate gives

$$r_{\mathrm{imp}}=\frac{(FK+AI(T))/100-1}{0.25}.$$

Using the quoted futures price of $115.3670$,

$$r_{\mathrm{imp}}=
\frac{(115.3670\times0.8624648692+1)/100-1}{0.25}
=0.0199993826.$$

$$\boxed{r_{\mathrm{imp}}\approx1.9999383\%\approx2\%.}$$

The small difference from exactly 2% results from rounding the futures quote to four decimal places. Using the unrounded normalized forward price from Question 1 gives exactly 2%.

### 2.2 Selecting the CTD bond

Implied repo measures the annualized return associated with buying a cash bond and delivering it against a short futures position. When funding conditions are comparable, the bond with the highest implied repo is generally the most attractive delivery candidate.

A direct comparison uses the clean forward acquisition cost. Under simple-interest financing and coupon reinvestment at the same rate,

$$BF_x^{\mathrm{clean}}=
P_x^{\mathrm{dirty}}(0)(1+r_x^{\mathrm{fin}}T)
-\sum_{0<t_i\le T}C_{x,i}[1+r_x^{\mathrm{fin}}(T-t_i)]
-AI_x(T).$$

Here, $r_x^{\mathrm{fin}}$ is the actual financing rate for bond $x$. The delivery profit per $100 face value is

$$\Pi_x=F K_x-BF_x^{\mathrm{clean}}.$$

The short selects the bond offering the highest delivery profit. If financing terms or reinvestment assumptions differ materially across bonds, this net-profit comparison is more reliable than ranking raw implied repo rates alone.

In the assignment's simplified pricing model,

$$F^*=\min_x\frac{BF_x^{\mathrm{clean}}}{K_x},\qquad
\mathrm{CTD}=\arg\min_x\frac{BF_x^{\mathrm{clean}}}{K_x}.$$

With a common market repo rate and a futures quote equal to this theoretical price, the CTD's implied repo equals the market repo rate. The other deliverable bonds have implied repo rates no greater than the market rate. Under those assumptions, the CTD is also the bond with the highest implied repo rate.

- If $r_{\mathrm{imp}}>r_{\mathrm{mkt}}$, borrowing at the market rate, purchasing the bond, and selling futures creates positive cash-and-carry profit in the frictionless model.
- If $r_{\mathrm{imp}}<r_{\mathrm{mkt}}$, buying and financing that bond for delivery fails to cover the funding cost. A short should prefer a more favorable delivery bond. This inequality alone does not establish an unrestricted reverse arbitrage for a non-CTD bond, since a futures long cannot choose which bond it receives.

The party choosing the deliverable bond is the futures short. The exchange administers the delivery process.

## 3. Scenario analysis

### 3.1 Predicting the CTD N days later

CTD changes can be predicted conditionally under specified market scenarios. A definite prediction requires the full deliverable basket, bond prices, financing rates, and assumptions about future market conditions.

For each scenario:

1. Keep the contract's delivery date and conversion factors fixed.
2. Advance the valuation date by N days, updating accrued interest, remaining cashflows, and time to delivery.
3. Reprice every deliverable bond using the assumed yield curve and relative-value changes.
4. Calculate its forward acquisition cost using the remaining coupon payments and relevant repo rate, including special financing conditions where applicable.
5. Compare $BF_x/K_x$ across the basket. The lowest value identifies the scenario CTD in the assignment's model.

For two candidates, the CTD switching boundary satisfies

$$\frac{BF_a}{K_a}=\frac{BF_b}{K_b}.$$

Parallel yield shifts, curve steepening or flattening, and changes in bond-specific repo rates can all change the ranking. Higher yields may favor longer-duration bonds because their cash prices typically fall more; lower yields may favor shorter-duration bonds. These are tendencies rather than universal rules, since conversion factors, carry, curve shape, and relative financing costs also matter.

### 3.2 Illustrative 30-day scenario

The following basket is constructed for illustration; it is not market data supplied by the assignment. Both bonds pay 4% semiannual coupons and initially have seven and nine years remaining, respectively. Delivery occurs three months from the initial valuation date. Repo remains at 2%, N is 30 days, and elapsed time is measured as $30/360$ years. Conversion factors remain fixed at their initial values.

| Yield after 30 days | 7Y bond normalized forward | 9Y bond normalized forward | Scenario CTD |
|---|---:|---:|---|
| 3% | 119.375599 | 124.601654 | 7Y bond |
| 4% | 112.356947 | 115.558358 | 7Y bond |
| 5% | 105.810391 | 107.270225 | 7Y bond |
| 6% | 99.701496 | 99.669374 | 9Y bond |
| 7% | 93.998507 | 92.694375 | 9Y bond |

The small difference at a 6% yield reflects financing carry and accrued interest. The conversion factor does not guarantee identical normalized forward prices at future valuation dates.

### 3.3 Why the final deliverable matters

- **Delivery profit:** The short has a delivery choice. Selecting a less favorable bond increases the cost of satisfying the contract.
- **Hedging:** While the CTD remains unchanged, it typically dominates futures price sensitivity. With consistent price and face-value units, a common approximation is $DV01_F\approx DV01_{\mathrm{CTD}}/K_{\mathrm{CTD}}$. A CTD switch can change the appropriate hedge ratio.
- **Basis and financing trades:** Net basis and implied repo returns depend on the bond ultimately delivered and its actual funding cost.
- **Delivery optionality:** The short's quality option affects futures valuation and risk near switching boundaries. Actual contracts can also involve delivery-timing options.

These calculations follow the assignment's treatment of a bond future as a standardized forward. They do not separately model daily margining or futures-forward differences caused by stochastic interest rates.

## Computational part: six TODO implementations

The repository's computational task is separate from the bond-futures questions. Its notebook asks for two cashflow product classes and a display visitor.

| TODO | Location | Implementation |
|---|---|---|
| 1 | Fixed cashflow constructor | Initialize the base cashflow, store accrual fields and conventions, default payment to termination, and calculate the accrual year fraction. |
| 2 | Overnight cashflow constructor | Retrieve the index, resolve a tenor using its calendar and business-day convention, obtain currency from the index, and store contract fields. |
| 3 | Fixed cashflow `accept` | Return `visitor.visit(self)`. |
| 4 | Overnight cashflow `accept` | Return `visitor.visit(self)`. |
| 5 | Fixed display visitor | Collect common fields followed by the six requested fixed-accrual fields. |
| 6 | Overnight display visitor | Collect common fields followed by the six requested overnight-index fields. |

`qfDisplayProduct(product)` creates the visitor and calls `product.accept(visitor)`. The product delegates to `visitor.visit(product)`, and `singledispatchmethod` selects the handler for the actual product class. The collected fields are returned as a Name/Value table.

For the fixed cashflow example, `accrued = 90/360 = 0.25` is a year fraction, not a cash amount. This class has no fixed-rate field. Similarly, the overnight product stores contract terms; computing its interest amount requires historical fixings or a forecasting curve.

The two modified upstream files are `fixedincomelib/product/linear_products.py` and `fixedincomelib/product/product_display_visitor.py`. The package includes `solution.patch` and the executed instructor notebook.

Source repository: [Jerry0108-SJ/FRE-GY-9743-Assignments-3](https://github.com/Jerry0108-SJ/FRE-GY-9743-Assignments-3), commit `5847d1b4860177e0b4747ecbd696e28edc7a4c14`.
