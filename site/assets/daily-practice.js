(() => {
  const root = document.getElementById("daily-practice-app");
  if (!root) return;
  const levels = {
    beginner: {
      words: [["arrive","To reach a place","I arrive at work at nine."],["borrow","To use something and return it","Can I borrow your pen?"],["careful","Taking care to avoid mistakes","Please be careful on the stairs."],["choose","To decide between options","Choose one answer."],["finish","To complete something","I finish my work on time."],["helpful","Ready to help","The new guard is helpful."],["invite","To ask someone to come","I will invite my friend."],["quiet","Making little or no noise","Please keep the room quiet."],["ready","Prepared for something","I am ready for duty."],["useful","Helpful for a purpose","This is a useful sentence."]],
      sentences:["I am ready for work.","Could you please help me?","Where is the nearest bus stop?","I will call you later.","Thank you for your time."],
      question:{q:"Choose the correct sentence.",options:["She go to work.","She goes to work.","She going to work."],answer:1,why:"Use goes with he, she and it in the present simple."},
      speaking:"Introduce yourself. Say your name, where you live and what you do."
    },
    intermediate: {
      words: [["achieve","To succeed in doing something","She achieved her target this month."],["arrange","To put things in order or plan them","Please arrange the files by date."],["confident","Sure about your ability","He feels confident while speaking."],["efficient","Working well without wasting time","An efficient team follows a clear plan."],["expect","To think something will happen","We expect the visitor at noon."],["maintain","To keep something in good condition","Maintain a clean work area."],["notice","To see or become aware of something","I noticed a change in the schedule."],["prevent","To stop something from happening","Good communication can prevent errors."],["respond","To answer or react","Please respond to the message."],["responsible","Having a duty to take care of something","Every team member is responsible for safety."]],
      sentences:["I will look into the matter and update you.","Could you clarify the instructions?","We need to complete this task before noon.","I appreciate your support.","Please let me know if anything changes."],
      question:{q:"Choose the best word: Clear instructions can ____ mistakes.",options:["prevent","expect","arrange"],answer:0,why:"Prevent means to stop something from happening."},
      speaking:"Describe a problem you solved at work. Explain the problem, your action and the result."
    },
    advanced: {
      words: [["anticipate","To expect something and prepare for it","We should anticipate possible delays."],["collaborate","To work together with others","The departments collaborate on safety planning."],["consequence","A result of an action","Every decision has a consequence."],["delegate","To give a task to another person","A supervisor must delegate tasks clearly."],["evaluate","To judge the quality or value","We will evaluate the results tomorrow."],["implement","To put a plan into action","The team will implement the new procedure."],["negotiate","To discuss to reach an agreement","They negotiated a revised schedule."],["prioritize","To decide what is most important first","Prioritize urgent requests."],["resolve","To find a solution to a problem","We need to resolve the issue quickly."],["transparent","Open and easy to understand","Keep communication transparent."]],
      sentences:["We need to assess the situation before taking action.","I would appreciate your feedback on this proposal.","Let us establish clear priorities for the day.","The issue has been resolved through coordination.","I will take responsibility for communicating the update."],
      question:{q:"Choose the closest meaning of 'prioritize'.",options:["Ignore a task","Decide what matters most first","Complete every task at once"],answer:1,why:"Prioritize means to arrange tasks by importance."},
      speaking:"Give a short opinion on why teamwork matters. Support it with two clear reasons and an example."
    }
  };
  const topics = ["Learn and Revise Basic English","Daily English Words Practice","Make Correct English Sentences","Is, Am and Are Practice","Speak About Yourself","Daily Routine Speaking Practice","Common English Questions","Basic Vocabulary Revision","Present Simple Tense Practice","Present Continuous Practice","Describe People and Places","English Conversation at Home","Listening Practice for Beginners","Past Simple Tense Practice","50 Useful English Verbs","Speak About Your Work","Asking Questions Confidently","Future Tense Practice","English at Shops and Markets","Pronunciation Improvement","Reading Short English Stories","Prepositions Practice","English Phone Conversations","Speak for 5 Minutes Daily","Mid-Year English Assessment","Articles and Determiners Practice","Describe Your Experiences","Workplace English Communication","Listening to Indian English","Modal Verbs Practice","English for Job Interviews","Writing Short Paragraphs","Vocabulary for Everyday Life","English Conversation with Strangers","Improve Sentence Formation","Understand Spoken English","Express Your Opinions","Active and Passive Voice Practice","English Email Writing","Storytelling in English","Advanced Daily Vocabulary","English Discussion Practice","Improve Fluency and Confidence","Mixed Grammar Revision","Listening and Speaking Test","Professional English Communication","Read and Explain English Texts","Speak Without Translating","Complete Vocabulary Revision","Real-Life Conversation Assessment","Complete English Grammar Test","Final 365-Day English Assessment"];
  const storageKey = "efg.dailyPractice.v1";
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch (_) {}
  let level = saved.level || "beginner";
  const today = new Date().toISOString().slice(0,10);
  const dayOfYear = Math.floor((new Date(today)-new Date(new Date().getFullYear(),0,0))/86400000);
  const topic = topics[Math.floor((dayOfYear-1)/7)%topics.length];
  const data = () => levels[level];
  const save = () => { saved.level=level; localStorage.setItem(storageKey,JSON.stringify(saved)); };
  const completed = () => saved.completed || {};
  const isDone = completed()[today] === true;
  const esc = s => String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function render(){
    const d=data();
    root.innerHTML = `
      <section class="daily-welcome"><span class="daily-eyebrow">YOUR DAILY 10-MINUTE ROUTINE</span><h1>Daily English Practice</h1><p>Small practice every day. Clear progress over time.</p><div class="daily-topic"><span>Today's topic from your 365-Day Practice</span><strong>${esc(topic)}</strong></div></section>
      <section class="daily-level-panel"><div><h2>Choose your level</h2><p>Change your level whenever you are ready.</p></div><div class="daily-levels" role="group" aria-label="English level">
      <button data-level="beginner" class="${level==="beginner"?"selected":""}">Beginner</button><button data-level="intermediate" class="${level==="intermediate"?"selected":""}">Intermediate</button><button data-level="advanced" class="${level==="advanced"?"selected":""}">Advanced</button></div></section>
      <section class="daily-progress"><div><strong>${Object.keys(completed()).length}</strong><span>Practice days completed</span></div><div><strong>${isDone?"Done":"10 min"}</strong><span>Today's progress</span></div><div><strong>${level[0].toUpperCase()+level.slice(1)}</strong><span>Current level</span></div></section>
      <section class="daily-step"><div class="daily-step-head"><span>01 · 3 MINUTES</span><h2>Vocabulary</h2><p>Read each word, meaning and example aloud.</p></div><div class="daily-word-grid">${d.words.map((w,i)=>`<article class="daily-word"><span>${String(i+1).padStart(2,"0")}</span><h3>${esc(w[0])}</h3><p>${esc(w[1])}</p><small>${esc(w[2])}</small></article>`).join("")}</div></section>
      <section class="daily-step"><div class="daily-step-head"><span>02 · 2 MINUTES</span><h2>Daily sentences</h2><p>Read these sentences clearly. Repeat each one twice.</p></div><ol class="daily-sentences">${d.sentences.map(x=>`<li>${esc(x)}</li>`).join("")}</ol></section>
      <section class="daily-step"><div class="daily-step-head"><span>03 · 2 MINUTES</span><h2>Quick test</h2><p>${esc(d.question.q)}</p></div><div class="daily-question">${d.question.options.map((o,i)=>`<button class="daily-option" data-answer="${i}">${esc(o)}</button>`).join("")}<p class="daily-feedback" aria-live="polite"></p></div></section>
      <section class="daily-step"><div class="daily-step-head"><span>04 · 3 MINUTES</span><h2>Speaking task</h2><p>Speak aloud for three minutes. Do not worry about small mistakes.</p></div><div class="daily-speaking"><p>${esc(d.speaking)}</p><button id="daily-speaking-done" type="button">I completed my speaking task</button></div></section>
      <section class="daily-finish"><div><h2>Finish today's practice</h2><p>Mark the session complete after vocabulary, sentences, test and speaking.</p></div><button id="daily-complete" ${isDone?"disabled":""}>${isDone?"Today's practice completed ✓":"Mark today complete"}</button></section>
      <section class="daily-progress-details" id="progress"><h2>My Progress</h2><p>Your progress is saved only in this browser. No account is required.</p><div class="daily-progress-bar"><span style="width:${Math.min(100,Object.keys(completed()).length/30*100)}%"></span></div><strong>${Object.keys(completed()).length} practice days recorded</strong></section>`;
    root.querySelectorAll("[data-level]").forEach(b=>b.addEventListener("click",()=>{level=b.dataset.level;save();render();}));
    root.querySelectorAll("[data-answer]").forEach(b=>b.addEventListener("click",()=>{root.querySelectorAll("[data-answer]").forEach(x=>x.disabled=true);const correct=Number(b.dataset.answer)===d.question.answer;b.classList.add(correct?"correct":"incorrect");root.querySelector(".daily-feedback").textContent=(correct?"Correct! ":"Not quite. ")+d.question.why;}));
    root.querySelector("#daily-speaking-done").addEventListener("click",e=>{e.currentTarget.textContent="Speaking task completed ✓";e.currentTarget.disabled=true;});
    root.querySelector("#daily-complete").addEventListener("click",()=>{saved.completed=completed();saved.completed[today]=true;save();render();});
  }
  render();
})();
