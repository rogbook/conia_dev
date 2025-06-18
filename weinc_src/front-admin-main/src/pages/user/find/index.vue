<template>
  <div class="mx-auto" style="max-width: 30rem">
    <!-- Card -->
    <div class="card card-lg mb-5">
      <div class="card-body text-center">
        <div class="mb-5">
          <h1 class="display-5">회원정보 찾기</h1>
          <p class="mb-0">아이디 찾기 또는 비밀번호 변경을 선택해 주세요.</p>
        </div>

        <div class="card-group">
          <div class="card">
            <div class="card-body">
              <RouterLink to="find/account">
                <h5 class="card-title">아이디 찾기</h5>
              </RouterLink>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <RouterLink to="find/password">
                <h5 class="card-title">비밀번호 변경</h5>
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="text-center">
          <a class="btn btn-link">
            <RouterLink to="/login"><i class="bi-chevron-left"></i> Back to Sign in</RouterLink>
          </a>
        </div>
      </div>
    </div>
    <!-- End Card -->
  </div>
</template>
