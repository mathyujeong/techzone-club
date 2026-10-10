import re

with open('src/app/admin/page.tsx', 'r') as f:
    admin = f.read()

# Replace the broken flex Settings Panel with the clean, unbreakable Grid layout
old_settings_panel = """              {/* --- TOP: SETTINGS PANEL --- */}
              <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm flex flex-col xl:flex-row gap-4 items-center shrink-0">
                
                <div className="flex flex-col sm:flex-row w-full flex-1 gap-4 items-center">
                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">경기 방식</label>
                    <select 
                      value={matchType} 
                      onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                      className="w-full sm:w-auto bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="TEAM">청백전 (팀전)</option>
                      <option value="INDIVIDUAL">개인전 (랜덤 매치)</option>
                    </select>
                  </div>

                  <div className="w-full sm:w-auto">
                    <label className="text-xs text-gray-500 font-bold mb-1 block">종목 선호</label>
                    <select 
                      value={genderPref} 
                      onChange={e => setGenderPref(e.target.value as 'SAME_GENDER' | 'MIXED')}
                      className="w-full sm:w-auto bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 px-3 py-2 rounded-xl font-bold outline-none cursor-pointer"
                    >
                      <option value="SAME_GENDER">남복/여복 우선 (추천)</option>
                      <option value="MIXED">혼복 포함 (랜덤)</option>
                    </select>
                  </div>

                  <div className="flex gap-2 w-full sm:w-auto">
                    <div className="flex-1 sm:w-24 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-1 flex flex-col justify-center">
                      <label className="text-[10px] text-gray-500 font-bold">코트 수</label>
                      <div className="flex items-center gap-1">
                        <input type="number" min="1" max="10" value={numCourts} onChange={e => setNumCourts(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-black outline-none text-lg" />
                        <span className="text-xs text-gray-400 font-bold">면</span>
                      </div>
                    </div>
                    <div className="flex-1 sm:w-24 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-1 flex flex-col justify-center">
                      <label className="text-[10px] text-gray-500 font-bold">총 라운드</label>
                      <div className="flex items-center gap-1">
                        <input type="number" min="1" max="20" value={numRounds} onChange={e => setNumRounds(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-black outline-none text-lg" />
                        <span className="text-xs text-gray-400 font-bold">R</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-row sm:flex-col gap-4 sm:gap-2 w-full sm:w-auto bg-gray-50 dark:bg-gray-800/50 p-2 rounded-xl">
                    <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer">
                      <input type="checkbox" checked={ignoreGrade} onChange={e => setIgnoreGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500" />
                      급수 무관 매칭
                    </label>

                  </div>
                </div>

                <div className="w-full xl:w-auto shrink-0">
                  <button 
                    onClick={handleGenerate}
                    disabled={isGenerating || selectedPlayerIds.size < 4}
                    className="w-full xl:w-64 bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-black flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md text-lg"
                  >
                    <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                    대진표 자동 짜기
                  </button>
                </div>
              </div>"""

new_settings_panel = """              {/* --- TOP: SETTINGS PANEL --- */}
              <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 sm:p-5 shadow-sm flex flex-col gap-4 shrink-0">
                
                {/* 1차 컨트롤 영역: 5개 항목 반응형 그리드 */}
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 items-end">
                  
                  {/* 1. 경기 방식 */}
                  <div className="flex flex-col gap-1 col-span-1">
                    <label className="text-xs text-gray-500 font-bold">경기 방식</label>
                    <select 
                      value={matchType} 
                      onChange={e => setMatchType(e.target.value as 'TEAM' | 'INDIVIDUAL')}
                      className="w-full bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-2.5 rounded-xl font-bold text-xs sm:text-sm outline-none cursor-pointer"
                    >
                      <option value="TEAM">청백전 (팀전)</option>
                      <option value="INDIVIDUAL">개인전 (랜덤)</option>
                    </select>
                  </div>

                  {/* 2. 종목 선호 */}
                  <div className="flex flex-col gap-1 col-span-1">
                    <label className="text-xs text-gray-500 font-bold">종목 선호</label>
                    <select 
                      value={genderPref} 
                      onChange={e => setGenderPref(e.target.value as 'SAME_GENDER' | 'MIXED')}
                      className="w-full bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 px-3 py-2.5 rounded-xl font-bold text-xs sm:text-sm outline-none cursor-pointer"
                    >
                      <option value="SAME_GENDER">남복/여복 우선</option>
                      <option value="MIXED">혼복 포함 (랜덤)</option>
                    </select>
                  </div>

                  {/* 3. 코트 수 */}
                  <div className="flex flex-col gap-1 col-span-1">
                    <label className="text-xs text-gray-500 font-bold">코트 수</label>
                    <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-1.5 rounded-xl h-[42px]">
                      <input type="number" min="1" max="10" value={numCourts} onChange={e => setNumCourts(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-black outline-none text-base text-center" />
                      <span className="text-xs text-gray-400 font-bold shrink-0">면</span>
                    </div>
                  </div>

                  {/* 4. 총 라운드 */}
                  <div className="flex flex-col gap-1 col-span-1">
                    <label className="text-xs text-gray-500 font-bold">총 라운드</label>
                    <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-1.5 rounded-xl h-[42px]">
                      <input type="number" min="1" max="20" value={numRounds} onChange={e => setNumRounds(parseInt(e.target.value) || 1)} className="w-full bg-transparent font-black outline-none text-base text-center" />
                      <span className="text-xs text-gray-400 font-bold shrink-0">R</span>
                    </div>
                  </div>

                  {/* 5. 급수 무관 매칭 */}
                  <div className="flex items-center justify-center h-[42px] px-3 bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl col-span-2 sm:col-span-1 whitespace-nowrap">
                    <label className="flex items-center gap-2 text-xs font-bold text-gray-700 dark:text-gray-300 cursor-pointer select-none">
                      <input type="checkbox" checked={ignoreGrade} onChange={e => setIgnoreGrade(e.target.checked)} className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 cursor-pointer" />
                      급수 무관 매칭
                    </label>
                  </div>

                </div>

                {/* 2차 버튼 영역: 풀 너비 메인 실행 버튼 */}
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-black flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md text-base"
                >
                  <RefreshCw className={`w-5 h-5 ${isGenerating ? 'animate-spin' : ''}`} />
                  대진표 자동 짜기
                </button>
              </div>"""

admin = admin.replace(old_settings_panel, new_settings_panel)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(admin)

