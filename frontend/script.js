/* ============================================================
   MindPulse — script.js
   Handles form validation, the /predict API call, and the
   animated Mental Health Score gauge on the right-hand panel.
   ============================================================ */

const API_URL = 'http://127.0.0.1:8000/predict';
const ARC_LENGTH = 314; // length of the semicircle path used in the gauge

const form = document.getElementById('checkinForm');
const submitBtn = document.getElementById('submitBtn');
const formError = document.getElementById('formError');

const stateEmpty = document.getElementById('stateEmpty');
const stateLoading = document.getElementById('stateLoading');
const stateResult = document.getElementById('stateResult');

const gaugeArc = document.getElementById('gaugeArc');
const gaugeNumber = document.getElementById('gaugeNumber');
const bandLabel = document.getElementById('bandLabel');
const poeticLine = document.getElementById('poeticLine');
const resetBtn = document.getElementById('resetBtn');

// Constraints mirrored from the Pydantic model, used for client-side validation
// so bad input is caught here instead of failing quietly at the API.
const RULES = {
  Age:                      { type: 'int',   gt: 5,  lt: 25 },
  Avg_Daily_Usage_Hours:    { type: 'int',   ge: 0,  le: 20 },
  Daily_Unlocks:            { type: 'float', gt: 0,  lt: 300 },
  Study_Hours:              { type: 'float', gt: 0,  lt: 16 },
  Physical_Activity_Hours:  { type: 'float', ge: 0,  lt: 20 },
  Sleep_Hours_Per_Night:    { type: 'float', gt: 1,  lt: 19 },
};

function showState(name){
  [stateEmpty, stateLoading, stateResult].forEach(el => el.classList.remove('is-active'));
  ({ empty: stateEmpty, loading: stateLoading, result: stateResult })[name].classList.add('is-active');
}

function validateField(id, value){
  const rule = RULES[id];
  if (!rule) return true;
  const num = Number(value);
  if (Number.isNaN(num)) return false;
  if (rule.type === 'int' && !Number.isInteger(num)) return false;
  if (rule.gt !== undefined && !(num > rule.gt)) return false;
  if (rule.ge !== undefined && !(num >= rule.ge)) return false;
  if (rule.lt !== undefined && !(num < rule.lt)) return false;
  if (rule.le !== undefined && !(num <= rule.le)) return false;
  return true;
}

function collectPayload(){
  const ids = [
    'Age', 'Gender', 'Country', 'Academic_Level', 'Most_Used_Platform',
    'Purpose_Of_Use', 'Avg_Daily_Usage_Hours', 'Daily_Unlocks', 'Study_Hours',
    'Physical_Activity_Hours', 'Sleep_Hours_Per_Night', 'Stress_Level'
  ];
  const payload = {};
  let firstInvalid = null;

  ids.forEach(id => {
    const el = document.getElementById(id);
    const raw = el.value;

    if (raw === ''){
      if (!firstInvalid) firstInvalid = el;
      return;
    }

    if (['Age','Avg_Daily_Usage_Hours'].includes(id)){
      payload[id] = parseInt(raw, 10);
    } else if (['Daily_Unlocks','Study_Hours','Physical_Activity_Hours','Sleep_Hours_Per_Night'].includes(id)){
      payload[id] = parseFloat(raw);
    } else {
      payload[id] = raw;
    }

    if (RULES[id] && !validateField(id, raw) && !firstInvalid){
      firstInvalid = el;
    }
  });

  return { payload, firstInvalid, complete: Object.keys(payload).length === ids.length };
}

// Poetic bands — evocative wording, kept honest and non-clinical.
function describeScore(score){
  if (score >= 8){
    return { band: 'Still water', line: "Your mind rests like still water tonight — steady, clear, unhurried." };
  }
  if (score >= 6){
    return { band: 'Finding rhythm', line: "You're finding your rhythm, though the tide still pulls a little." };
  }
  if (score >= 4){
    return { band: 'Some weather', line: "There's some weather moving through you today — nothing you can't ride out." };
  }
  return { band: 'A loud storm', line: "The storm's been loud lately. Go gently, and reach out to someone if you need to." };
}

function renderResult(score){
  const clamped = Math.max(0, Math.min(10, score));
  const { band, line } = describeScore(clamped);

  gaugeNumber.textContent = clamped.toFixed(1);
  bandLabel.textContent = band;
  poeticLine.textContent = line;

  const offset = ARC_LENGTH - (clamped / 10) * ARC_LENGTH;
  gaugeArc.style.transition = 'none';
  gaugeArc.setAttribute('stroke-dashoffset', ARC_LENGTH);

  showState('result');

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      gaugeArc.style.transition = 'stroke-dashoffset 1000ms cubic-bezier(.2,.8,.2,1)';
      gaugeArc.setAttribute('stroke-dashoffset', offset);
    });
  });
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  formError.classList.remove('show');
  formError.textContent = '';

  const { payload, firstInvalid, complete } = collectPayload();

  if (!complete || firstInvalid){
    formError.textContent = 'Please fill in every field with a value in range.';
    formError.classList.add('show');
    if (firstInvalid) firstInvalid.focus();
    return;
  }

  submitBtn.disabled = true;
  showState('loading');

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok){
      const text = await res.text().catch(() => '');
      throw new Error(`Server responded ${res.status}: ${text}`);
    }

    const data = await res.json();
    const score = data.Mental_health_score ?? data.mental_health_score;

    if (typeof score !== 'number'){
      throw new Error('Unexpected response shape from the API.');
    }

    renderResult(score);

  } catch (err){
    showState('empty');
    formError.textContent = "Couldn't reach the model — make sure your FastAPI server is running on http://127.0.0.1:8000.";
    formError.classList.add('show');
    console.error(err);
  } finally {
    submitBtn.disabled = false;
  }
});

resetBtn.addEventListener('click', () => {
  showState('empty');
});